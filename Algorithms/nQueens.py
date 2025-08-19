
def rec_nQueens(size, queens=None):
    """
    Recursively computes all solutions for the n-Queens puzzle.

    :param size: The size of the puzzle
    :type size: int
    :param queens: The currently placed queens, e.g. [4,2] represent
    that on row 0 there is a queen on the 4th index and on row 1 
    there is a queen on the 2nd index. 
    :type queens: list[int]
    
    :return: the (partial) list of queen posisitons
    :rtype: list[int]
    """
    if queens is None:
        queens = []
        
    if len(queens) == size:
        return [queens]
    
    solutions = []
    for col in range(size):
        if constraint(queens, col):
            new_queens = queens + [col]
            solutions += rec_nQueens(size, new_queens)
    
    return solutions

def constraint(queens, col):
    """
    The constraints for the n-queens problem.

    :param queens: The currently placed queens.
    :type queens: list[int]
    :param col: The column that the next queen would be placed
    :type col: int

    :return: If the puzzle constraint is satisfied or not
    :rtype: bool
    """
    new_row = len(queens)
    for i in range(len(queens)):
        if queens[i] == col:
            return False
        if abs(i - new_row) == abs(queens[i] - col):
            return False


    return True

