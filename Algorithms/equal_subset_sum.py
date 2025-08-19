import copy
import typing
import timeit
import random
import matplotlib.pyplot as plt

"""
In this assignment, we make 4 variations of the equal subset sum problem.
In the script below, you can find some timing tests to see what the difference is that these variation make in time.

The equal subset sum problem asks if a set of numbers can be split into two groups with equal sums. 
It explores different ways to divide the numbers and checks if any division results in equal totals.

Note 1, each number is seen as unique thus [1', 1''] has two solutions: ([1'], [1'']) and ([1''], [1']), the apostrophes 
are their just to visualize how the solutions are different in your code you would see ([1], [1]) and ([1], [1]).   

Note 2, left and right are considered different so the solution ([3], [1, 2]) is not the same as ([1, 2], [3]).

You have to complete/use all three functions that are given, see hint. 

Before you start try to figure out how you would tackle this problem on paper and describe the algorithm in words.

Hint: Two helper functions are given to either solve it "normal" or "all" 
      both have a flag to solve it with or without backtracking. 
      However, if you find the flags difficult, you can also make 4 extra helper functions 
      that are called from the two helper functions with flags. For example:
      def ess_normal(data, left, right, backtracking=True):
          if backtracking:
              return ess_normal_bt(data, left, right)
          return ess_normal_exh(data, left, right)
          
      def ess_normal_bt(data, left, right):
          ...
          
      def ess_normal_exh(data, left, right):
          ...
          
"""

def equal_subset_sum(data, algorithm="normal"):
    """
    This function returns the outcome of the equal subset sum problem.
    The outcome may vary depending on the selected algorithm:
        - normal, use exhaustive DFS to find one solution, rtype -> tuple[list[int], list[int]]
        - normal_bt, use DFS with backtracking to find on solution, rtype -> tuple[list[int], list[int]]
        - all, use exhaustive DFS to find all solutions, rtype -> list[tuple[list[int], list[int]]]
        - all_bt, use DFS with backtracking to find all solutions, rtype -> list[tuple[list[int], list[int]]]

    If there is no solution the output should be a comparable datatype but with empty lists.
    So either a tuple with empty lists or a list with one tuple that has empty lists.

    :param data: The original list with the values
    :type data: list[int]
    :param algorithm: A string telling the function which algorithm to use.
    :type algorithm: str
    :return: One solution is: A tuple of two list of equal sum or two empty lists. All solutions are: a list of solutions
    :rtype: tuple[list[int], list[int]] or list[tuple[list[int], list[int]]]
    """
    if algorithm == "normal":
        result = ess_normal(data, [], [])
    elif algorithm == "normal_bt":
        result = ess_normal(data, [], [], backtracking=True)
    elif algorithm == "all":
        result = ess_all(data, [], [])
    elif algorithm == "all_bt":
        result = ess_all(data, [], [], backtracking=True)
    else:
        raise ValueError("Unknown algorithm. Please use 'normal', 'normal_bt', 'all' or 'all_bt'.")
    
    if algorithm in ("all", "all_bt") and not result:
        return [([], [])]
    return result

def ess_normal(data, left, right, backtracking=False):
    """
    One Divide & Conquer step for the equal subset sum problem to find one solution.

    :param data: The original list with the values
    :type data: list[int]
    :param left: The left sub list.
    :type left: list[int]
    :param right: The right sub list.
    :type right: list[int]
    :param backtracking: If backtracking is enabled or not
    :type backtracking: bool
    :return: Two list of equal sum or two empty lists.
    :rtype: tuple[list[int], list[int]]
    """
    if len(data) == 0:
            if sum(left) == sum(right):
                return left, right
            else:
                return [], []
    if backtracking:
        if sum(left) - sum(right) > sum(data):
            return [], []
        if sum(right) - sum(left) > sum(data):
            return [], []
        left.append(data[0])
        result = ess_normal(data[1:], left, right, backtracking)
        if result != ([], []):
            return result
        left.pop()
        right.append(data[0])
        result = ess_normal(data[1:], left, right, backtracking)
        if result != ([], []):
            return result
        right.pop()
    else: 
        left.append(data[0])
        result = ess_normal(data[1:], left, right, backtracking)
        if result != ([], []):
            return result
        left.pop()
        right.append(data[0])
        result = ess_normal(data[1:], left, right, backtracking)
        if result != ([], []):
            return result
        right.pop()
    
    return [], []
        

def ess_all(data, left, right, backtracking=False):
    """
    One Divide & Conquer step for the equal subset sum problem to find all solutions.

    :param data: The original list with the values
    :type data: list[int]
    :param left: The left sub list.
    :type left: list[int]
    :param right: The right sub list.
    :type right: list[int]
    :param backtracking: If backtracking is enabled or not
    :type backtracking: bool
    :return: Two list of equal sum or two empty lists.
    :rtype: list[tuple[list[int], list[int]]] or list[]
    """
    if len(data) == 0:
        if sum(left) == sum(right):
            return [(left.copy(), right.copy())]
        else:
            return []
    if backtracking:
        if sum(left) - sum(right) > sum(data):
            return []
        if sum(right) - sum(left) > sum(data):
            return []
        left.append(data[0])
        result = ess_all(data[1:], left, right, backtracking)
        left.pop()
        right.append(data[0])
        result += ess_all(data[1:], left, right, backtracking)
        right.pop()
    else: 
        left.append(data[0])
        result = ess_all(data[1:], left, right, backtracking)
        left.pop()
        right.append(data[0])
        result += ess_all(data[1:], left, right, backtracking)
        right.pop()
    
    return result

def time_equal_subset_sum(list_sizes=range(16), log=True):
    """
    This function is for visualization purposes only.
    So you can ignore it.
    """
    algorithms = ["normal", "normal_bt", "all", "all_bt"]  # Algorithms to test
    colors = {
        "normal": "blue",
        "normal_bt": "green",
        "all": "red",
        "all_bt": "purple"
    }
    offsets = {
        "normal": -0.15,
        "normal_bt": -0.05,
        "all": 0.05,
        "all_bt": 0.15
    }

    # Data structure to store times for each algorithm and list size
    times = {algorithm: {size: [] for size in list_sizes} for algorithm in algorithms}

    # Create random lists of different sizes using random
    for size in list_sizes:
        print(f"Testing list of size {size}")

        for algorithm in algorithms:
            # Run the test for 20 different lists, repeating the test 20 times
            total_times = timeit.repeat(
                stmt=f"equal_subset_sum([random.randint(1, 10) for _ in range({size})], '{algorithm}')",
                setup="from __main__ import random, equal_subset_sum",
                number=1,
                repeat=20
            )

            # Store the individual execution times for scatter plot
            times[algorithm][size] = total_times

            avg_time = sum(total_times) / len(total_times)
            print(f"Algorithm: {algorithm}, Average Time: {avg_time:.6f} seconds")

    # Plot the results
    plt.figure(figsize=(10, 6))

    for algorithm in algorithms:
        color = colors[algorithm]
        offset = offsets[algorithm]

        # Scatter plot with offset
        for size in list_sizes:
            x_jittered = [size + offset] * len(times[algorithm][size])
            plt.scatter(x_jittered, times[algorithm][size],
                        alpha=0.1, color=color, label=f"{algorithm} data" if size == list_sizes[0] else "")

        # Line plot for average (aligned with true x values)
        avg_times = [sum(times[algorithm][size]) / len(times[algorithm][size]) for size in list_sizes]
        plt.plot(list_sizes, avg_times, color=color, label=f"{algorithm} average")

    # Log scale y-axis
    if log:
        plt.yscale('log')

    # Labels & legend
    plt.xlabel('List Size')
    plt.ylabel('Time (seconds, log scale)')
    plt.title('Equal Subset Sum Timing')

    plt.legend()
    plt.tight_layout()
    plt.savefig("timings.png")


if __name__ == "__main__":
    print(equal_subset_sum([1, 1, 3, 5, 2]))
    print(equal_subset_sum([1, 5, 2]))
    print(equal_subset_sum([1, 1, 3, 5, 2], 'normal_bt'))
    print(equal_subset_sum([1, 5, 2], 'normal_bt'))
    print(equal_subset_sum([1, 1, 3, 5, 2], 'all'))
    print(equal_subset_sum([1, 5, 2], 'all'))
    print(equal_subset_sum([1, 1, 3, 5, 2], 'all_bt'))
    print(equal_subset_sum([1, 5, 2], 'all_bt'))

    TIMING = False
    if TIMING:
        """
        you can change the sizes of the lists that are tested and if log scale is used.
        Just note that it can take a while to run it for more then 20 numbers.
        
        Also, think about why there seems to be to sets of data points for normal but not for all?
        """
        time_equal_subset_sum()