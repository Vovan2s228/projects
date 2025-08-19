def greedy_coin_change(coins, amount):
    """
    Use a greedy algorithm to make change for a given amount, 
    there is no limit on the amount of times you can use the same coins. 
    
    For example, given coins = [1, 4, 6] and amount = 8 
    the problem is (greedily) solved by returning the list: [6,1,1]
    
    :param coins: list of coins (e.g. [25, 10, 5, 1])
    :type coins: List[Int]
    :amount: the total amount to make change for
    :return: list of coins used (Empty list if no solution)
    """
    
    coins.sort(reverse=True)
    result = []

    for coin in coins:
        while amount >= coin:
            amount -= coin
            result.append(coin)

    if amount != 0:
        return []
    return result

