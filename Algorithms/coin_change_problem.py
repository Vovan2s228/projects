import copy
import typing

"""
Another problem that could be solved with Divide and Conquer is the coin change problem. 
In this problem, we want to find all ways to give change back for a certain amount given some specified coins. 

In the coin problem, we have an unlimited amount of coins of the following type: 
1 cent, 2 cents, 5 cents, 10 cents, 20 cents, 50 cents, 1 euro, and 2 euros. 
The goal is to find all ways to give change for a certain amount so, for example,
if we want to give change for 5 cents we can do that in 4 ways: 
5x 1 cent, 3x 1 cent + 1x 2 cents, 1x 1 cent + 2x 2 cents, and 1x 5 cents. 
 
Note, that there is no order in which we give the change. 
So, the only thing that matters is what coins and how many of these coins we use.

Try to come up with a pseudo-algorithm that uses Divide and Conquer to solve this problem. 
The idea should be similar to the equal subset problem where you split the problem into two sub-problems, 
where in one case you choose to use the largest coin and in the other case you don't.
"""

class CoinChange():
    """
    A class attribute for the coins is here the correct approach as
    this list should not change and is for all object the same.
    Note: that you can access the coins either through CoinChange.coins (recommended) or obj.coins,
          where obj inside the class is often self and outside the class can be named anything.
    """
    coins = (2, 1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01)

    def __call__(self, amount):
        """
        This method calculates all possible ways to give change for the amount.

        :param amount: The amount that is the sum of the change.
        :type amount: float
        :return: A list with all possible ways to give change. The change consists of a list of coins.
        :rtype: list[list[float]]
        """
        self.result = []
        total_cents = int(round(amount * 100))
        self.step(total_cents, [], 0)
        return self.result

    def step(self, leftover_amount, change, max_coin_id):
        """
        One recursive step in the divide and conquer algorithm.

        Hint: We are doing arithmetic with floats, do you think a value would always be exactly zero or not?

        :param leftover_amount: The leftover amount of change. This is the original amount minus the change.
        :type leftover_amount: float
        :param change: A list of coins.
        :type change: list[float]
        :param max_coin_id: The index of the largest coin that this step can use.
        :type max_coin_id: int
        :return: A list with all possible ways to give change. The change consists of a list of coins.
        :rtype: list[list[int]]
        """
        if leftover_amount == 0:
            self.result.append([c / 100 for c in change])
            return

        if leftover_amount < 0 or max_coin_id >= len(self.coins):
            return

        coin_value = int(round(self.coins[max_coin_id] * 100))

        if coin_value > leftover_amount:
            self.step(leftover_amount, change, max_coin_id + 1)
            return

        change.append(coin_value)
        self.step(leftover_amount - coin_value, change, max_coin_id)
        change.pop()

        self.step(leftover_amount, change, max_coin_id + 1)


if __name__ == "__main__":
    change_solver = CoinChange()
    print(change_solver(0.05))
