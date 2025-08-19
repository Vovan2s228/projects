def shortest_edit_distance(A: str, B: str) -> int:
    """
    The goal is to turn the string A into the string B by a sequence of moves.
    There are three possible moves:
        1. Deletion: delete one letter from string A.
        2. Insertion: insert one letter into string A.
        3. Mutation: change one letter from A to a different one.
    This function returns the lowest possible number of moves to turn A into B.

    Do this by using dynamic programming.

    Hint: Complete the Least Common Subsequence problem first. 

    Hint: Solve the recurrence relation first. 
    What would be the subproblems and what variables would you need. 

    :param A: The string that is to be modified into B.
    :type A: str
    :param B: The string that A must be modified into.
    :type B: str
    :return: The lowest possible amount of moves to modify A into B.
    :rtype: int
    """

    n = len(A)
    m = len(B)
    dp = [[0] * (m+1) for k in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n+1):
        for j in range(1, m+1):
            if A[i-1] == B[j-1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j - 1] + 1, dp[i - 1][j] + 1, dp[i][j - 1] + 1)
    return dp[n][m]
