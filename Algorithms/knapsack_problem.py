def knapsack_bottom_up(weights, values, capacity):
    """
    Given a Knapsack with a maximum capacity and a list of items with their respective weights and values,
    the objective is to find a sequence of items that maximizes the total value without exceeding the weight limit.

    For example, consider these items:
    - Item 1: weight = 2, value = 6
    - Item 2: weight = 3, value = 10
    - Item 3: weight = 3, value = 12

    If the maximum weight capacity of the knapsack is 5, the optimal solution is to take items 1 and 3, giving a total value of 18.
    For more detailed information, refer to the slides on Brightspace.


    This function implements the 0/1 Knapsack problem using a bottom-up dynamic programming approach.
    It calculates the maximum value that can be obtained by selecting items with given weights and values
    without exceeding the maximum weight capacity of the knapsack.
   
    :param weights: A list of integers representing the weights of the items.
    :type weights: list[int]
    :param values: A list of integers representing the values of the items. So to get e.g. the first item, 
    you can use values[0] to get the value and weights[0] to get the weight.
    
    :type values: list[int]
    :returns: The maximum value that can be obtained within the weight limit.
    :rtype: int
    """

    n = len(values)
    # dp[i][w] = max value using first i items and capacity w
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        wi = weights[i-1]
        vi = values[i-1]
        for w in range(capacity + 1):
            if wi <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w-wi] + vi)
            else:
                dp[i][w] = dp[i-1][w]

    return dp[n][capacity]