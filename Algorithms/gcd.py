"""
Euler's algorithm for finding the greatest common divisor (GCD) is based on the principle that
the GCD of two numbers a and b is the same as the GCD of b and a mod b.
This works because if a number d divides both a and b, it must also divide the remainder
when a is divided by b (which is a mod b).
This process is repeated until b becomes zero, at which point the GCD is the value of a.

For more information you can go to the wiki link: https://en.wikipedia.org/wiki/Euclidean_algorithm

Implement the Euclidean algorithm below, but before you begin try to understand why this is decrease by variable size and conquer.
"""

def gcd(a, b):
    """
    This function calculates the greatest common divisor of a and b.
    """
    if a == 0:
        return b
    elif b == 0:
        return a
    else:
        return gcd(b, a % b)


if __name__ == "__main__":
    a = 10002
    b = 10001
    print(f"The greasest common divisor of {a} and {b} is {gcd(a, b)}.")  # Note, the gcd of 1071 and 462 is 21.
