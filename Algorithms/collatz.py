def collatz_bottom_up(n):
    """
    The Collatz Conjecture is one of the most famous unsolved puzzles in mathemmatics.

    The conjecture states that the following two operations, on any number positive integer, 
    will eventually produce the number 1: 

    	OP1: If the number is even, divide by two 
    	OP2: If the number is odd, multiple by 3 and add 1.
    	
    ex1. For the number 4: 
    	f(4)= 2 -> f(2)=1, which satisfy the condition 
	ex2. For the number 5: 
    	f(5)=15+1 -> f(16)=8 -> f(4) -> ... -> 1, which also satisfies the condition. 

    We call the sequence of operations above a "Collatz Sequence". 

    Using bottom-up Dynamic Programming, determine the length of the longest Collatz Sequence 
    out of all numbers 0 through n. 

    :param n: The upper limit for the Collatz sequence
    :return: The length of the longest Collatz sequence for a number in the range 1 to n (included)
    :rtype: int
    """

    if n == 0:
        return 0
    dp = {1: 1}
    for i in range(2, n + 1):
        j = i
        count = 0
        while j not in dp:
            count += 1
            if j % 2 == 0:
                j //= 2
            else:
                j = 3 * j + 1
        dp[i] = count + dp[j]
    return max(dp.values())