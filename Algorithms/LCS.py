import numpy as np

def longest_common_subsequence(X,Y):
    """
    Calculates the length of the longest common subsequence of strings X and Y
    
    A sequence, is an ordered collection of objects which may contain duplicates. 
    
   	A subsequence of a sequence, is a sequence that can be obtained by deleting 
    some elements without changing their order. 
    
    For example: (1,2,4,6,0,-1) has (1,0,-1) and (6,-1) as subsequences. 
    
	We will consider a string as a sequences of its characters (in order). 
	
    For example, the strings "ABCD" and "CADB" have the following subsequences in common: 
    "A", "B", "C", "D",
    "AB", "CD", and "AC"
    
    Hint: Use two variables. 
    
    :param X: The first string
    :param Y: The second string
    :return: The length of the longest common subsequence
    :rtype: int
    """

    m = len(X)
    n = len(Y)
    dp = [[0] * (n + 1) for k in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]