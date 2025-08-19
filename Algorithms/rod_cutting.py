from functools import cache
def cut_rod(price):
    """
    Given a list of prices where price[i] is the price of a rod of length i+1,
    return the maximum price obtainable by cutting up the rod and selling the pieces.
    Use dynamic programming to speed up the solution.
    Use tabulation (bottom-up) or memoization (top-down) to solve this problem.
    
    Arguments:
    price -- List[int], where price[i] = price of rod length i+1

    Returns:
    int -- Maximum price obtainable
    """
    
    n = len(price)

    @cache
    def max_price(length: int) -> int:
        if length == 0:
            return 0
        best = 0
        # try all first-cut lengths i = 1..length
        for i in range(1, length + 1):
            best = max(best, price[i-1] + max_price(length - i))
        return best

    return max_price(n)