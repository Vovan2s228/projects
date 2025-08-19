from lock_ring import LockCombinationPuzzle

"""
In this assignment, you need to write an exhaustive search algorithm that finds the right lock combination to open the lock.
Each lock has a number of rings. Each ring can have x amount of options.
Exhaustive search for this assignment can be done by rotating a ring, 
check if the lock is open if not repeat the previous steps.
For example if we would have a lock with 2 rings and 2 options per ring the combinations would be:
1 1
1 2
2 1
2 2

In this assignment, you have to interacted with a lock object given in the lock_ring.py file.
A lock object has 3 useful methods/functions that can help you:
 - lock.turn_ring(n), this turns the n'th ring once and returns if the ring is in the original position or not.
 - lock.check_open(), this checks if the lock is open or not.
 - len(lock) can be used to know how many rings a lock has. 
"""

def solve_lock_combination_problem(lock):
    """
    This method solves the lock with "n" rings problem.

    :param lock: The lock that needs to be opened.
    :type lock: lockRingPuzzle
    :return: This function does not have a return, as the lock object is changed.
    :rtype: None
    """
    solve_lock_combination_recursive(lock, 0)
    

def solve_lock_combination_recursive(lock, ring):
    """
    This is one step in the exhaustive search algorithm which uses depth-first search.

    :param lock: The lock that needs to be opened.
    :type lock: lockRingPuzzle
    :param ring: The ring that is currently turned.
    :type ring: int
    :return: If the lock is opened in the current configuration.
    :rtype: boolean
    """
    if ring == len(lock):
        return lock.check_open()
    for _ in range(7):  # Enough turns to cover ring sizes up to 7
        if solve_lock_combination_recursive(lock, ring + 1):
            return True
        lock.turn_ring(ring)
    return False
    

"""
You can find an example below to check if your code works.
"""
if __name__ == "__main__":
    lock = LockCombinationPuzzle()
    solve_lock_combination_problem(lock)
    print(lock.check_open(), lock)
