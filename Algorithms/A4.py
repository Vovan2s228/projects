import numpy as np
import typing
from copy import *


################################# Part I: ITERATIVE DFS ######################################
"""
Implement an iterative DFS algorithm which takes an adjacency list representation, 
of a directed connected graph, and returns True or False whether the graph has a cycle
"""

def DFS_is_acyclic(adj_list: typing.Dict[int, typing.List[int]]) -> bool:
    """
    
    :param adj_list: The adjacency list representation of the graph
    :return: True if the graph is acyclic, False otherwise
    """	
    #initialize stack
    visited = set()
    stack = []
    for start in adj_list:
        if start in visited:
            continue
        #initialize a stack for the current path
        path_stack = []
        stack.append((start, 0))
        path_stack.append(start)

        while stack:
            node, child_index = stack[-1]
            #if there are still unvisited children, keep exploring
            if child_index < len(adj_list[node]):
                child = adj_list[node][child_index]
                stack[-1] = (node, child_index + 1)
                #if child was already encountered -> cycle
                if child in path_stack:
                    return False
                #if not-> keep searching
                if child not in visited:
                    stack.append((child, 0))
                    path_stack.append(child)
            #remove the child from search stack if no cycle is found
            else:
                stack.pop()
                visited.add(node)
                path_stack.pop()

    return True
    



################################# Part II: ROWS AND COLUMNS #####################################
"""
We consider the following two player game. It is played with m*n checkers pieces, that are positioned in an m times n rectangle (m rows and n columns). 

There are two players, V (Vertical) and H (Horizontal), that take turns making a move, V always makes the first move. The player who removes the last piece wins.
A move for V constitutes removing a column, a move for H constitutes removing a row. Removing a row or column from  the rectangle generally splits it in two smaller rectangles, unless the row or column was removed from the edge. At the start of the game, there is only one square, but this number grows. A player on turn removes
one row (H) or column (V) from exactly one of the rectangles. Consider the following sequence of moves, for m = 3 and n = 4 (here, the pieces are represented by X's, and different rectangles are separated by commas):

X X X X   V   X   X X   H  X           V   X            H  X
X X X X  -->  X , X X  --> X, X X, X X --> X , X X , X --> X , X
X X X X       X   X X      X               X               X
  (*)                                                      (**)

It’s V’s turn to move in (**). If she removes the column with 3 pieces, she will lose. Suppose she removes the column with one piece, then that leaves a winning position for H (Why?). Therefore, state (**) is losing for V.

Implement a function that takes a list of two arguments: [(m, n)] and returns whether the game is winning for H = 1, or V = 0
"""

def Row_Columns(gameState, player):
    """
    :param gameState: A list of tuples representing the size of the (sub)boards
    :param player: The player on turn, 1 for H and 0 for V
    
    :return: 1 if H has a winning strategy, 0 if V has a winning strategy       
    """
    #initialize memory
    memo = {}
    #make the statespace equivalent if the rectangles are of the same size
    def canonical(state):
        return tuple(sorted(state))
    #a recusive search to go through states back to the first player. whenever an equivalent state is encountered, skip to result
    def is_winning(state, player):
        state = canonical(state)
        if (state, player) in memo:
            return memo[(state, player)]

        if not state:
            memo[(state, player)] = False
            return False
        #initialize game and game rules
        for i, (m, n) in enumerate(state):
            moves = []
            if player == 0:
                for c in range(n):
                    if c == 0 or c == n - 1:
                        new_board = (m, n-1) if (n-1) > 0 else None
                        move_result = []
                        if new_board is not None:
                            move_result.append(new_board)
                    else:
                        left = (m, c) if c > 0 else None
                        right = (m, n - c - 1) if (n - c - 1) > 0 else None
                        move_result = []
                        if left is not None:
                            move_result.append(left)
                        if right is not None:
                            move_result.append(right)
                    moves.append(move_result)
            else:
                for r in range(m):
                    if r == 0 or r == m - 1:
                        new_board = (m-1, n) if (m-1) > 0 else None
                        move_result = []
                        if new_board is not None:
                            move_result.append(new_board)
                    else:
                        top = (r, n) if r > 0 else None
                        bottom = (m - r - 1, n) if (m - r - 1) > 0 else None
                        move_result = []
                        if top is not None:
                            move_result.append(top)
                        if bottom is not None:
                            move_result.append(bottom)
                    moves.append(move_result)
            #log the state
            remaining = list(state[:i] + state[i+1:])
            for move_result in moves:
                new_state = remaining + move_result
                if not is_winning(tuple(new_state), 1 - player):
                    memo[(state, player)] = True
                    return True

        memo[(state, player)] = False
        return False

    return player if is_winning(tuple(gameState), player) else 1 - player
