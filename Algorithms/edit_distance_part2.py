from functools import cache

def bottom_up_shortest_edit_distance(a:str, b:str) -> int:
    """
    
    The goal is to turn the string A into the string B by a sequence of moves.
    There are three possible moves:
        1. Deletion: delete one letter from string A.
        2. Insertion: insert one letter into string A.
        3. Mutation: change one letter from A to a different one.
    This function returns the lowest possible number of moves to turn A into B.
    
    Do this by using bottom up dynamic programming.

    Hint: Solve the recurrence relation first. 
    What would be base case subproblems that you can solve without any smaller sub problems?
      
    :param A: The string that is to be modified into B.
    :type A: str
    :param B: The string that A must be modified into.
    :type B: str
    :return: The lowest possible amount of moves to modify A into B.
    :rtype: int
    """

    n = len(a)
    m = len(b)
    dp = [[0] * (m+1) for k in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n+1):
        for j in range(1, m+1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j - 1] + 1, dp[i - 1][j] + 1, dp[i][j - 1] + 1)
    return dp[n][m]