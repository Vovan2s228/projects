"""
Write a function to calculate n! factorial recursively.

Think about what a subproblem is and how this is decrease by one and conquer.
"""

def factorial_recursion(n):
    """
    This function calculates the nth factorial recursively.

    :param n: The nth factorial number
    :type n: int
    :return: n!
    :type: int
    """
    if n <= 1:
        return 1
    else:
        return n * factorial_recursion(n-1)


if __name__ == "__main__":
    n = 4
    print(f"{n}! = {factorial_recursion(n)}")