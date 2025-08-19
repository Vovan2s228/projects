def knapsack_greedy(weights, values, capacity):
    """
    Greedy algorithms are not always optimal, but they are faster and can be used as a heurstic, 
    i.e. a non-exact or "good enough" solution, for when an exact solution is not required.

    In this exercise your task is to implement a greedy algorithm for the 0/1 Knapsack Problem
    (it's called 0/1 because each item is used 0 or 1 times) 

    Hint: Choose the items based on the value-to-weight ratio.


    :param weights: A list of integers representing the weights of the items.
    :type weights: list[int]
    :param values: A list of integers representing the values of the items. So to get e.g. the first item, 
    you can use values[0] to get the value and weights[0] to get the weight.
    
    :type values: list[int]
    :return: The maximum value that can be obtained within the weight limit using the greedy approach.
    :rtype: int
    """
    
    ratios = [(values[i] / weights[i], weights[i], values[i])
              for i in range(len(values))]

    ratios.sort(key=lambda x: x[0], reverse=True)

    total_value = 0
    for ratio, wt, val in ratios:
        if wt <= capacity:
            capacity -= wt
            total_value += val

    return total_value