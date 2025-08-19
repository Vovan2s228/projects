"""
In lab 2, we tackled binary search trees which are a good datastructure to do binary search in.
In this lab, we will do binary search on an order list.

Binary search works by repeatedly dividing the search space in half.
At each step, we compare the middle element with the target value and decide whether to search the left or right half.
This process continues recursively until the value is found or the search space is empty.

The framework below contains a class that functions as a function with the added benifit that you can split the algorithm into two parts.
First part is the call method that takes a list and value and stores it as attributes and call the first recursive step.
The recursive step only needs two value the lower and upper boundary for that step and returns the index of the value
This is done by recursively calling step with smaller boundaries.
The advantage of a class it that everything is encapsulated and you can have more methods with less arguments.

Implement the binary search algorithm below, but before you begin try to understand why this is decrease by constant factor and conquer.
"""

class BinarySearch():
    """
    A binary search class that can be used to make a callable object
    which given a list and a value returns the index of the value.

    After __call__ the object has two attributes:
        :param sorted_list: A sorted list with values.
        :type list: list
        :param value: The value that you are searching for.
        :type value: int
    """
    def __call__(self, sorted_list, value):
        """
        This method finds the index of a value in a list
        if a list does not have the value you should return None.

        :param sorted_list: A sorted list with values.
        :type sorted_list: list[int]
        :param value: The value that you are searching for.
        :type value: int
        :return: index of the found value.
        :rtype: int
        """
        self.sorted_list = sorted_list
        self.value = value
        return self.step(0, len(sorted_list) - 1)

    def step(self, min_index, max_index):
        """
        This is one step in the binary search algorithm.
        No helper methods are given but if you want you can create
        for example a next_step method or base_case method.

        :param min_index: The left index of your search space, thus the minimum value of your search space.
        :type min_index: int
        :param max_index: The right index of your search space, thus the maximum value of your search space.
        type max_index: int
        :return: index of the found value.
        :rtype: int
        """

        if min_index > max_index:
            return None
        mid = (min_index + max_index) // 2
        if self.sorted_list[mid] == self.value:
            return mid
        elif self.value < self.sorted_list[mid]:
            return self.step(min_index, mid - 1)
        else:
            return self.step(mid + 1, max_index)


if __name__ == "__main__":
    search_func = BinarySearch()
    lst = [0, 2, 3, 5, 8, 10]
    print(f"in the list: {lst} the value 3 is at index {search_func(lst, 3)}")
    print(f"in the list: {lst} the value 7 is at index {search_func(lst, 7)}")

