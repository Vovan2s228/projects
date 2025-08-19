#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Standard-library-only Amazon scraper + keyword scorer, hardened.

Scoring formula:
  score(word) = sum_items( count(word in item) * (rating/5)^2 * (reviews)^(exp) )
Default exp = 0.2 (i.e., 1/5) per your spec. Change with --reviews-exp.

usage: scraping.py [-h] [--keyword KEYWORD] [--top TOP] [--mobile] [--no-mobile] [--verbose] [--trace] [--reviews-exp REVIEWS_EXP] [--search-pages SEARCH_PAGES]
                   [--max-competitors MAX_COMPETITORS] [--min-final MIN_FINAL] [--delay-min DELAY_MIN] [--delay-max DELAY_MAX] [--timeout TIMEOUT] [--no-summary]        
                   client
Usage example:
    python scraping.py B0CZMSJ8PP --mobile --verbose --trace --no-summary
"""

import sys
import re
import time
import random
import argparse
import json
import http.cookiejar as cookiejar
from html.parser import HTMLParser
from urllib import request, parse, error

# -----------------------------
# Defaults (overridable via CLI)
# -----------------------------
DEFAULT_SEARCH_RESULTS_PAGES = 1         # gentle default to reduce bot checks
DEFAULT_MAX_COMPETITOR_FETCH = 10
DEFAULT_MIN_FINAL_COMPETITORS = 8
DEFAULT_REQUEST_TIMEOUT = 20
DEFAULT_DELAY_MIN = 3.0
DEFAULT_DELAY_MAX = 6.0
DEFAULT_REVIEWS_EXP = 0.3                # your spec: (reviews)^(1/5)

FILLER = {
    "the","and","of","a","is","to","for","with","which","your",
    "on","in","it","or","an","by","as","at","be","that","this",
    "from","are","has","have","you","we","our","us"
}

# Domains
AMAZON_DOMAIN_DESKTOP = "www.amazon.com"
AMAZON_DOMAIN_MOBILE  = "m.amazon.com"

# CLI-adjusted globals (set in main())
VERBOSE = False
TRACE = False
USE_MOBILE = True
SEARCH_RESULTS_PAGES = DEFAULT_SEARCH_RESULTS_PAGES
MAX_COMPETITOR_FETCH = DEFAULT_MAX_COMPETITOR_FETCH
MIN_FINAL_COMPETITORS = DEFAULT_MIN_FINAL_COMPETITORS
REQUEST_TIMEOUT = DEFAULT_REQUEST_TIMEOUT
REQUEST_DELAY_RANGE = (DEFAULT_DELAY_MIN, DEFAULT_DELAY_MAX)
REVIEWS_EXPONENT = DEFAULT_REVIEWS_EXP

# Sticky session
CJ = cookiejar.CookieJar()
OPENER = request.build_opener(request.HTTPCookieProcessor(CJ))
STICKY_UA = random.choice([
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
])

# -----------------------------
# Diagnostics summary container
# -----------------------------
_SUMMARY = {
    "client": {},
    "discovery": {"derived_keyword": False, "keyword_used": None, "search_pages_scanned": 0},
    "filters": {"strict_filter_used": False, "relaxed_filter_used": False, "strict_count": 0, "final_count": 0},
    "items": [],  # per item diagnostics
}

def vprint(*a, **k):
    if VERBOSE:
        print(*a, **k)

def tprint(*a, **k):
    if TRACE:
        print(*a, **k)

def add_item_diag(item, **flags):
    _SUMMARY["items"].append({
        "asin": item.asin,
        "title_snippet": (item.title or "")[:80],
        "rating": item.rating,
        "reviews": item.reviews,
        **flags
    })

# -----------------------------
# Domain / URL helpers
# -----------------------------
def current_domain():
    return AMAZON_DOMAIN_MOBILE if USE_MOBILE else AMAZON_DOMAIN_DESKTOP

def build_product_url(asin: str) -> str:
    if USE_MOBILE:
        return f"https://{current_domain()}/gp/aw/d/{asin}"
    return f"https://{current_domain()}/dp/{asin}"

def search_url(keyword: str, page: int) -> str:
    q = parse.quote(keyword)
    return f"https://{current_domain()}/s?k={q}&page={page}"

def extract_asin_from_url(url: str) -> str:
    m = re.search(r"/([A-Z0-9]{10})(?:[/?]|$)", url)
    return m.group(1) if m else ""

def is_asin(s: str) -> bool:
    return bool(re.fullmatch(r"[A-Z0-9]{10}", s.strip().upper()))

# -----------------------------
# CAPTCHA detection (multi-signal)
# -----------------------------
PRODUCT_MARKERS = [
    r'id="productTitle"',             # desktop title
    r'class="a-icon-alt"',            # desktop rating text container
    r"<h1[^>]*>",                     # mobile title
    r"out of\s*5\s*stars",            # mobile rating text
]

def detect_captcha(html: str, *, require_multiple=True):
    """
    Heuristic CAPTCHA detector.
    Returns: (is_captcha: bool, reasons: [str])
    """
    if not html:
        return False, ["empty_html"]

    lc = html.lower()

    groups = [
        (["/errors/validatecaptcha", 'action="/errors/validatecaptcha"', "/captcha/"], "captcha_endpoint"),
        (['name="amzn"', 'name="amzn-r"', 'id="amzn"', 'id="amzn-r"'], "hidden_amzn_fields"),
        (['id="captchacharacters"', 'name="captchacharacters"', 'id="ap_captcha_img"',
          'id="captchaimg"', 'id="captchaimage"', 'class="captcha"'], "captcha_widgets"),
        (['not a robot', 'enter the characters', 'type the characters', 'characters you see',
          'for security reasons', 'unusual traffic', 'are you a human', 'bot check', 'challenge'], "captcha_phrases"),
    ]

    matched = []
    for patterns, label in groups:
        if any(p in lc for p in patterns):
            matched.append(label)

    has_product_marker = any(re.search(p, lc, flags=re.S) for p in PRODUCT_MARKERS)

    if "service unavailable" in lc and "captcha" in lc:
        matched.append("503_service_unavailable_captcha")

    if matched:
        if require_multiple:
            if len(set(matched)) >= 2:
                return True, matched
            if len(set(matched)) == 1 and not has_product_marker:
                return True, matched
        else:
            return True, matched

    if not has_product_marker:
        if re.search(r'<form[^>]+/errors/validateCaptcha', lc) or re.search(r'<img[^>]+captcha', lc):
            return True, ["no_product_markers+captcha_like_form"]

    return False, []

# -----------------------------
# Requests: sticky UA + cookies + backoff
# -----------------------------
def fetch(url: str, *, max_retries: int = 3) -> str:
    # polite delay
    time.sleep(random.uniform(*REQUEST_DELAY_RANGE))

    headers = {
        "User-Agent": STICKY_UA,
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Connection": "keep-alive",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "Referer": f"https://{current_domain()}/",
    }

    last_html = ""
    for attempt in range(1, max_retries + 1):
        tprint(f"[FETCH] {url} (attempt {attempt}/{max_retries})")
        req = request.Request(url, headers=headers)
        try:
            with OPENER.open(req, timeout=REQUEST_TIMEOUT) as resp:
                charset = resp.headers.get_content_charset() or "utf-8"
                html = resp.read().decode(charset, errors="ignore")
        except error.HTTPError as e:
            html = e.read().decode("utf-8", errors="ignore") if e.fp else ""
        except Exception:
            html = ""

        last_html = html
        is_cap, reasons = detect_captcha(html)
        if is_cap:
            vprint(f"! CAPTCHA detected ({', '.join(reasons)}) on attempt {attempt}. Backing off...")
            sleep_s = 10 * attempt + random.uniform(2, 7)
            time.sleep(sleep_s)
            try:
                headers["Referer"] = url.rsplit("/", 1)[0] + "/"
            except Exception:
                pass
            continue

        return html

    return last_html  # may still be captcha; caller logs in summary

# -----------------------------
# HTML text extraction
# -----------------------------
class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self._chunks = []
        self._skip = False
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self._skip = True
    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript"):
            self._skip = False
    def handle_data(self, data):
        if not self._skip:
            txt = data.strip()
            if txt:
                self._chunks.append(txt)
    def text(self):
        return " ".join(self._chunks)

def html_to_text(fragment: str) -> str:
    parser = TextExtractor()
    parser.feed(fragment or "")
    return parser.text()

# -----------------------------
# Parsing helpers (desktop + mobile fallbacks)
# -----------------------------
def extract_title(html: str) -> str:
    m = re.search(r'id="productTitle"[^>]*>(.*?)</span>', html, flags=re.S|re.I)
    if m:
        return " ".join(html_to_text(m.group(1)).split())
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, flags=re.S|re.I)  # mobile
    if m:
        return " ".join(html_to_text(m.group(1)).split())
    return ""

def extract_rating_reviews(html: str):
    rating = None
    reviews = None
    rating_fallback_used = False

    # desktop rating
    m = re.search(r'data-hook="rating-out-of-text"[^>]*>(.*?)</span>', html, flags=re.S|re.I)
    txt = html_to_text(m.group(1)) if m else ""
    mm = re.search(r"([0-9.]+)\s*out of\s*5", txt)

    if not mm:
        m2 = re.search(r'class="a-icon-alt"[^>]*>(.*?)</span>', html, flags=re.S|re.I)
        txt2 = html_to_text(m2.group(1)) if m2 else ""
        mm = re.search(r"([0-9.]+)\s*out of\s*5", txt2)
        if mm:
            rating_fallback_used = True

    if not mm:
        m3 = re.search(r"([0-9.]+)\s*out of\s*5\s*stars", html, flags=re.I)  # mobile
        if m3:
            mm = m3
            rating_fallback_used = True

    if mm:
        try:
            rating = float(mm.group(1))
        except:
            rating = None

    # reviews
    m = re.search(r'id="acrCustomerReviewText"[^>]*>(.*?)</span>', html, flags=re.S|re.I)
    txt = html_to_text(m.group(1)) if m else ""
    mm = re.search(r"([\d,]+)", txt)
    if not mm:
        m2 = re.search(r"([\d,]+)\s+global\s+ratings", html, flags=re.I)  # mobile
        mm = m2
    if mm:
        try:
            reviews = int(mm.group(1).replace(",", ""))
        except:
            reviews = None

    return rating, reviews, rating_fallback_used

def extract_feature_bullets(html: str) -> str:
    m = re.search(r'id="feature-bullets"[^>]*>(.*?)</ul>', html, flags=re.S|re.I)
    if not m:
        return ""
    fragment = m.group(1)
    lis = re.findall(r"<li[^>]*>(.*?)</li>", fragment, flags=re.S|re.I)
    parts = [html_to_text(x) for x in lis]
    return " ".join(parts)

def extract_aplus(html: str) -> str:
    m = re.search(r'id="aplus_feature_div"[^>]*>(.*?)</div>\s*</div>', html, flags=re.S|re.I)
    return html_to_text(m.group(1)) if m else ""

def extract_product_description(html: str) -> str:
    m = re.search(r'id="productDescription"[^>]*>(.*?)</div>', html, flags=re.S|re.I)
    return html_to_text(m.group(1)) if m else ""

def extract_full_description(html: str):
    bullets = extract_feature_bullets(html)
    aplus = extract_aplus(html)
    pd = extract_product_description(html)
    pieces = [p for p in (bullets, aplus, pd) if p]
    desc = " ".join(pieces).strip()
    desc = re.sub(r"\s+", " ", desc)
    description_fallback_used = (len(pieces) == 0)
    return desc, description_fallback_used

# -----------------------------
# Search result parsing
# -----------------------------
def search_asins(keyword: str, pages=1):
    asins = []
    pages_scanned = 0
    for p in range(pages):
        url = search_url(keyword, p + 1)
        html = fetch(url)
        pages_scanned += 1
        for m in re.finditer(r"/dp/([A-Z0-9]{10})", html):
            asin = m.group(1)
            if asin not in asins:
                asins.append(asin)
        if len(asins) >= MAX_COMPETITOR_FETCH:
            break
    return asins[:MAX_COMPETITOR_FETCH], pages_scanned

# -----------------------------
# Tokenization & scoring
# -----------------------------
def tokenize(text: str):
    return re.findall(r"[a-zA-Z']+", (text or "").lower())

def count_words(text: str, filler: set):
    counts = {}
    for w in tokenize(text):
        if w in filler:
            continue
        counts[w] = counts.get(w, 0) + 1
    return counts

def item_factor(rating, reviews, reviews_exp: float):
    try:
        r = float(rating) if rating is not None else 0.0
    except:
        r = 0.0
    try:
        v = int(reviews) if reviews is not None else 0
    except:
        v = 0
    return (max(0.0, min(5.0, r)) / 5.0) ** 2 * (v ** (reviews_exp) if v > 0 else 0.0)

# -----------------------------
# Product model
# -----------------------------
class Item:
    __slots__ = ("asin","url","title","description","rating","reviews")
    def __init__(self, asin="", url="", title="", description="", rating=None, reviews=None):
        self.asin = asin
        self.url = url
        self.title = title
        self.description = description
        self.rating = rating
        self.reviews = reviews

def fetch_product(url_or_asin: str) -> Item:
    if is_asin(url_or_asin):
        asin = url_or_asin.upper()
        url = build_product_url(asin)
    else:
        url = url_or_asin
        asin = extract_asin_from_url(url) or ""

    html = fetch(url)

    is_cap, reasons = detect_captcha(html)
    if is_cap:
        vprint(f"! CAPTCHA still present on product page: {url}  reasons=({', '.join(reasons)})")

    title = extract_title(html)
    desc, desc_fallback = extract_full_description(html)
    rating, reviews, rating_fallback = extract_rating_reviews(html)

    item = Item(asin=asin, url=url, title=title, description=desc, rating=rating, reviews=reviews)
    add_item_diag(
        item,
        captcha_detected=is_cap,
        captcha_reasons=reasons if is_cap else [],
        rating_fallback_used=rating_fallback,
        description_fallback_used=desc_fallback,
        fields_missing={
            "title": not bool(title),
            "description": not bool(desc),
            "rating": rating is None,
            "reviews": reviews is None
        }
    )
    if rating_fallback:
        vprint(f"* Rating fallback used for ASIN {asin or 'UNKNOWN'}")
    if desc_fallback:
        vprint(f"* Description fallback used for ASIN {asin or 'UNKNOWN'} (no bullets/A+/description found)")
    return item

# -----------------------------
# Discovery & filtering
# -----------------------------
def discover_competitors(client: Item, keyword_hint: str | None):
    derived_keyword = False
    if not keyword_hint:
        words = [w for w in tokenize(client.title) if w not in FILLER]
        keyword_hint = " ".join(words[:6]) if words else "cast iron teapot"
        derived_keyword = True

    asins, pages_scanned = search_asins(keyword_hint, pages=SEARCH_RESULTS_PAGES)
    items = []
    for a in asins:
        if a == client.asin:
            continue
        it = fetch_product(build_product_url(a))
        if it.title:
            items.append(it)
        if len(items) >= MAX_COMPETITOR_FETCH:
            break

    _SUMMARY["discovery"]["derived_keyword"] = derived_keyword
    _SUMMARY["discovery"]["keyword_used"] = keyword_hint
    _SUMMARY["discovery"]["search_pages_scanned"] = pages_scanned
    if derived_keyword:
        vprint(f"* Derived keyword from client title: '{keyword_hint}'")
    else:
        vprint(f"* Using provided keyword: '{keyword_hint}'")
    return items

def filter_competitors(items: list, client: Item):
    cr = client.rating or 0.0
    cv = client.reviews or 0

    strict = [it for it in items if (it.rating or 0) >= cr and (it.reviews or 0) >= cv]
    _SUMMARY["filters"]["strict_count"] = len(strict)

    if len(strict) >= MIN_FINAL_COMPETITORS:
        strict.sort(key=lambda x: ((x.rating or 0), (x.reviews or 0)), reverse=True)
        final = strict[:MIN_FINAL_COMPETITORS]
        _SUMMARY["filters"]["strict_filter_used"] = True
        vprint(f"* Strict filter used (>= rating {cr}, >= reviews {cv}); kept {len(final)}")
        return final

    relaxed = [it for it in items if ((it.rating or 0) >= cr) or ((it.reviews or 0) >= cv)]
    relaxed.sort(key=lambda x: ((x.rating or 0), (x.reviews or 0)), reverse=True)
    final = relaxed[:MIN_FINAL_COMPETITORS]
    _SUMMARY["filters"]["relaxed_filter_used"] = True
    vprint(f"* Relaxed filter used (>= rating OR >= reviews); kept {len(final)} (strict had {len(strict)})")
    return final

# -----------------------------
# Scoring
# -----------------------------
def compute_scores(items: list, reviews_exp: float):
    scores = {}
    for it in items:
        text = f"{it.title} {it.description}"
        wc = count_words(text, FILLER)
        factor = item_factor(it.rating, it.reviews, reviews_exp)
        if factor == 0.0:
            continue
        for w, c in wc.items():
            scores[w] = scores.get(w, 0.0) + c * factor
    return scores

# -----------------------------
# Main
# -----------------------------
def main():
    global VERBOSE, TRACE, USE_MOBILE, SEARCH_RESULTS_PAGES, MAX_COMPETITOR_FETCH
    global MIN_FINAL_COMPETITORS, REQUEST_TIMEOUT, REQUEST_DELAY_RANGE, REVIEWS_EXPONENT

    ap = argparse.ArgumentParser(description="Amazon keyword scorer (stdlib) with strong CAPTCHA detection.")
    ap.add_argument("client", help="Client product URL or ASIN")
    ap.add_argument("--keyword", help="Optional search keyword (else derived from client title)")
    ap.add_argument("--top", type=int, default=30, help="How many top words to show (default 30)")
    ap.add_argument("--mobile", action="store_true", help="Use mobile pages (recommended)")
    ap.add_argument("--no-mobile", action="store_true", help="Force desktop pages")
    ap.add_argument("--verbose", action="store_true", help="Print fallbacks and warnings")
    ap.add_argument("--trace", action="store_true", help="Print every fetched URL")
    ap.add_argument("--reviews-exp", type=float, default=DEFAULT_REVIEWS_EXP, help="Exponent for reviews^exp (spec: 0.2)")
    ap.add_argument("--search-pages", type=int, default=DEFAULT_SEARCH_RESULTS_PAGES, help="Search result pages to scan")
    ap.add_argument("--max-competitors", type=int, default=DEFAULT_MAX_COMPETITOR_FETCH, help="Max competitor product fetches")
    ap.add_argument("--min-final", type=int, default=DEFAULT_MIN_FINAL_COMPETITORS, help="Minimum final competitors")
    ap.add_argument("--delay-min", type=float, default=DEFAULT_DELAY_MIN, help="Min delay between requests (sec)")
    ap.add_argument("--delay-max", type=float, default=DEFAULT_DELAY_MAX, help="Max delay between requests (sec)")
    ap.add_argument("--timeout", type=int, default=DEFAULT_REQUEST_TIMEOUT, help="HTTP timeout (sec)")
    ap.add_argument("--no-summary", action="store_true", help="Disable JSON diagnostics summary at end")
    args = ap.parse_args()

    VERBOSE = args.verbose
    TRACE = args.trace
    USE_MOBILE = args.mobile or (not args.no_mobile)  # mobile by default unless --no-mobile
    SEARCH_RESULTS_PAGES = max(1, args.search_pages)
    MAX_COMPETITOR_FETCH = max(1, args.max_competitors)
    MIN_FINAL_COMPETITORS = max(1, args.min_final)
    REQUEST_TIMEOUT = max(5, args.timeout)
    REVIEWS_EXPONENT = float(args.reviews_exp)
    dmin = max(0.0, args.delay_min)
    dmax = max(dmin + 0.1, args.delay_max)
    REQUEST_DELAY_RANGE = (dmin, dmax)

    # 1) client
    client_arg = args.client if args.client.startswith("http") else build_product_url(args.client)
    client = fetch_product(client_arg)
    if not client.title:
        sys.exit("Failed to fetch client product or parse its title.")
    print(f"Client: {client.title}\n  Rating={client.rating}  Reviews={client.reviews}  ASIN={client.asin}\n")
    _SUMMARY["client"] = {"asin": client.asin, "rating": client.rating, "reviews": client.reviews}

    # 2) competitors
    cand = discover_competitors(client, args.keyword)
    if not cand:
        sys.exit("No competitors discovered from search.")
    comps = filter_competitors(cand, client)
    if not comps:
        sys.exit("No competitors matched the popularity/rating filter (try --keyword, or relax limits).")

    print(f"Using {len(comps)} competitors:")
    for i, it in enumerate(comps, 1):
        print(f"{i:02d}. {it.title[:100]}…  Rating={it.rating}  Reviews={it.reviews}  ASIN={it.asin}")
    print()

    # 3) scores across client + competitors
    all_items = [client] + comps
    scores = compute_scores(all_items, REVIEWS_EXPONENT)

    top_n = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:max(1, args.top)]
    print(f"Top {len(top_n)} non-filler words (word — score):")
    for w, s in top_n:
        print(f"{w:20s} {s:.2f}")

    if not args.no_summary:
        _SUMMARY["filters"]["final_count"] = len(comps)
        print("\n=== SUMMARY (diagnostics) ===")
        print(json.dumps(_SUMMARY, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
