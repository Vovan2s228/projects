############ CODE BLOCK 0 ################
# DO NOT CHANGE THIS CELL.
# THESE ARE THE ONLY IMPORTS YOU ARE ALLOWED TO USE:

import numpy as np
import copy

RNG = np.random.default_rng()

############ CODE BLOCK 10 ################
class Sudoku():
    """
    This class creates sudoku objects which can be used to solve sudokus. 
    A sudoku object can be any size grid, as long as the square root of the size is a whole integer.
    To indicate that a cell in the sudoku grid is empty we use a zero.
    A sudoku object is initialized with an empty grid of a certain size.

    Attributes:
        :param self.grid: The sudoku grid containing all the digits.
        :type self.grid: np.ndarray[(Any, Any), int]  # The first type hint is the shape, and the second one is the dtype. 
        :param self.size: The width/height of the sudoku grid.
        :type self.size: int
    """
    def __init__(self, size=9):
        self.grid = np.zeros((size, size))
        self.size = size
        
    def __repr__(self):
        """
        This returns a representation of a Sudoku object.

        :return: A string representing the Sudoku object.
        :rtype: str
        """
        # Change this to anything you like, such that you can easily print a Sudoku object.
        return f"{self.grid}" 

############ CODE BLOCK 11 ################
    def set_grid(self, grid):
        """
        This method sets a new grid. This also can change the size of the sudoku.

        :param grid: A 2D numpy array that contains the digits for the grid.
        :type grid: ndarray[(Any, Any), int]
        """
        self.grid = grid
        # take the first row of the grid and assign its length to the size of the sudoku
        self.size = len(grid[0])

############ CODE BLOCK 12 ################
    def get_row(self, row_id):
        """
        This method returns the row with index row_id.

        :param row_id: The index of the row.
        :type row_id: int
        :return: A row of the sudoku.
        :rtype: np.ndarray[(Any,), int]
        """
        return self.grid[row_id]

    def get_col(self, col_id):
        """
        This method returns the column with index col_id.

        :param col_id: The index of the column.
        :type col_id: int
        :return: A row of the sudoku.
        :rtype: np.ndarray[(Any,), int]
        """
        return self.grid[:,col_id]

    def get_box_index(self, row, col):
        """
        This returns the box index of a cell given the row and column index.
        
        :param col: The column index.
        :type col: int
        :param row: The row index.
        :type row: int
        :return: This returns the box index of a cell.
        :rtype: int
        """
        # because for example col 3 refers to the 4th column if we start counting from 1
        col = col + 1
        row = row + 1
        box_size = int(np.sqrt(self.size))
        # create a 1D numpy array containing all the box indices
        numbers = np.arange(1, box_size * box_size + 1)
        # convert the 1D numpy array into a 2D matrix containing all the box indices in the correct positions
        matrix_box_indices = numbers.reshape(box_size, box_size)
        # obtain the location of the box index in the x-axis (with respect to matrix_box_indices)
        col_quotient = col // box_size
        col_remainder = col % box_size

        if col_remainder == 0:
            col_index = col_quotient - 1
        else:
            col_index = col_quotient
        # obtain the location of the box index in the y-axis (with respect to matrix_box_indices)
        row_quotient = row // box_size
        row_remainder = row % box_size
        
        if row_remainder == 0:
            row_index = row_quotient - 1
        else:
            row_index = row_quotient
        # search and return the box index
        return matrix_box_indices[row_index, col_index]

    def get_box(self, box_id):
        """
        This method returns the "box_id" box.

        :param box_id: The index of the sudoku box.
        :type box_id: int
        :return: A box of the sudoku.
        :rtype: np.ndarray[(Any, Any), int]
        """
        box_size = int(np.sqrt(self.size))
        # find which column the box is in
        box_id_location_xaxis = box_id % box_size
        # find which row the box is in
        box_id_location_yaxis = box_id // box_size

        if box_id_location_xaxis != 0:
            # add 1 to box_id_location_yaxis since the box is already at the next row
            box_id_location_yaxis += 1

        if box_id_location_xaxis == 0:
            # if box_id_location_xaxis is 0 it means the box is located at the right-most column
            box_id_location_xaxis = box_size
            
        # knowing the exact location of the box we use slicing on the grid to obtain the contents of the box
        return self.grid[(box_id_location_yaxis-1) * box_size:(box_id_location_yaxis-1) * box_size + box_size,(box_id_location_xaxis-1) * box_size:(box_id_location_xaxis-1) * box_size + box_size]

############ CODE BLOCK 13 ################
    @staticmethod
    def is_set_correct(numbers):
        """
        This method checks if a set (row, column, or box) is correct according to the rules of a sudoku.
        In other words, this method checks if a set of numbers contains duplicate values between 1 and the size of the sudoku.
        Note, that multiple empty cells are not considered duplicates.

        :param numbers: The numbers of a sudoku's row, column, or box.
        :type numbers: np.ndarray[(Any, Any), int] or np.ndarray[(Any, ), int]
        :return: This method returns if the set is correct or not.
        :rtype: Boolean
        """
        empty_list = []
        # check whether numbers is a 1D array
        if len(numbers.shape) == 1:
            for number in numbers:
                if number != 0:
                    if number not in empty_list:
                        empty_list.append(number)
                    else:
                        return False
            return True
        # check for duplicates when numbers is a 2D array
        for row in numbers:
            for number in row:
                if number != 0:
                    if number not in empty_list:
                        empty_list.append(number)
                    else:
                        return False
        return True

    def check_cell(self, row, col):
        """
        This method checks if the cell, denoted by row and column, is correct according to the rules of sudoku.
        
        :param col: The column index that is tested.
        :type col: int
        :param row: The row index that is tested.
        :type row: int
        :return: This method returns if the cell, denoted by row and column, is correct compared to the rest of the grid.
        :rtype: boolean
        """
        # check if there is a duplicate number in the column
        full_column = Sudoku.get_col(self, col)
        if Sudoku.is_set_correct(full_column) is False:
            return False
        # check if there is a duplicate number in the row
        full_row = Sudoku.get_row(self, row)
        if Sudoku.is_set_correct(full_row) is False:
            return False
        # check if there is a duplicate number in the box the cell belongs to
        box_id = Sudoku.get_box_index(self, row, col)
        box = Sudoku.get_box(self, box_id)
        if Sudoku.is_set_correct(box) is False:
            return False
        return True

    def check_sudoku(self):
        """
        This method checks, for all rows, columns, and boxes, if they are correct according to the rules of a sudoku.
        In other words, this method checks, for all rows, columns, and boxes, if a set of numbers contains duplicate values between 1 and the size of the sudoku.
        Note, that multiple empty cells are not considered duplicates.

        Hint: It is not needed to check if every cell is correct to check if a complete sudoku is correct.

        :return: This method returns if the (partial) Sudoku is correct.
        :rtype: Boolean
        """
        # check if all columns contain unique numbers
        for col_index in range(self.size):
            full_column = Sudoku.get_col(self, col_index)
            if Sudoku.is_set_correct(full_column) is False:
                return False
        # check if all rows contain unique numbers:
        for row_index in range(self.size):
            full_row = Sudoku.get_row(self, row_index)
            if Sudoku.is_set_correct(full_row) is False:
                return False
        # check if all the boxes contain unique numbers:
        for box_index in range(1, self.size + 1):
            box = Sudoku.get_box(self, box_index)
            if Sudoku.is_set_correct(box) is False:
                return False
        return True

############ CODE BLOCK 14 ################
    def step(self, row=0, col=0, backtracking=False):
        """
        This is a recursive method that completes one step in the exhaustive search algorithm.
        A step should contain at least, filling in one number in the sudoku and calling "next_step" to go to the next step.
        If the current number for this step does not give a correct solution another number should be tried 
        and if no numbers work the previous step should be adjusted.
        
        Hint 1: Numbers, that are already filled in should not be overwritten.
        Hint 2: Think about a base case.
    
        :param col: The current column index.
        :type col: int
        :param row: The current row index.
        :type row: int
        :param backtracking: This determines if backtracking is used. For now, this can be ignored. It defaults to False.
        :type backtracking: boolean, optional
        :return: This method returns if a correct solution can be found using this step.
        :rtype: boolean
        """
            
        if self.grid[row, col] == 0:
            for num in range(1, self.size + 1):
                self.grid[row, col] = num
                if self.check_cell(row, col) and self.next_step(row, col):
                    return True
                self.clean_up(row, col)
            return False
        else:
            return self.next_step(row, col)


    def next_step(self, row, col):
        """
        This method calculates the next step in the recursive exhaustive search algorithm.
        This method should only determine which cell should be filled in next.
        
        :param col: The current column index.
        :type col: int
        :param row: The current row index.
        :type row: int
        :param backtracking: This determines if backtracking is used. For now, this can be ignored. It defaults to False.
        :type backtracking: boolean, optional
        :return: This method returns if a correct solution can be found using this next step.
        :rtype: boolean
        """
        next_col = col + 1
        next_row = row
        if next_col == self.size:
            next_col = 0
            next_row += 1
        if next_row == self.size:
            return True
        return self.step(next_row, next_col)
    
    def clean_up(self, row, col):
        """
        This method cleans up the current cell if no solution can be found for this cell.
        
        :param col: The current column index.
        :type col: int
        :param row: The current row index.
        :type row: int
        :return: This method returns if a correct solution can be found using this next step.
        :rtype: boolean
        """
        self.grid[row, col] = 0
    
    def solve(self, backtracking=False):
        """
        Solve the sudoku using recursive exhaustive search.
        This is done by calling the "step" method, which does one recursive step.
        This can be visualized as a process tree, where "step" completes the functionality of of node.
        
        This method is already implemented and you do not have to do anything here.

        :param backtracking: This determines if backtracking is used. For now, this can be ignored. It defaults to False.
        :type backtracking: boolean, optional
        :return: This method returns if a correct solution for the whole sudoku was found.
        :rtype: boolean
        """
        return self.step(backtracking=backtracking)


############ END OF CODE BLOCKS, START SCRIPT BELOW! ################
