def floor_is_lava(grid, position, final_position, n, dp):
    """
    Calculates the probability of reaching the final_position from the given position
    in exactly n steps, moving only to adjacent (up, down, left, right) non-lava cells.

    Parameters:
    -----------
    grid : List[List[int]]
        A 2D list representing the map. A value of 1 indicates a safe cell,
        and 0 indicates a lava cell that cannot be stepped on.

    position : Tuple[int, int]
        The starting coordinates (x, y) in the grid.

    final_position : Tuple[int, int]
        The target coordinates (fx, fy) in the grid to reach in exactly n steps.

    n : int
        The exact number of steps allowed to reach the final position.

    dp : dict
        A memoization dictionary to cache subproblem results for optimization.
        Keys are tuples of the form (x, y, steps_remaining), and values are 
        computed probabilities for those states.

    Returns:
    --------
    float
        The probability of reaching the final_position from position in exactly n steps,
        moving only to adjacent safe cells with equal probability in each direction.

    Notes:
    ------
    - If a move would go out of bounds or onto lava, it contributes 0 to the probability.
    - At each step, the function tries all four directions (up/down/left/right) with equal probability (0.25).
    - If n == 0, the function returns 1.0 only if the current position is the final position,
      otherwise returns 0.0.
    """

    x, y = position
    key = (x, y, n)
    if key in dp:
        return dp[key]
    if n == 0:
        dp[key] = 1.0 if position == final_position else 0.0
        return dp[key]

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    total = 0.0
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 1:
            total += 0.25 * floor_is_lava(grid, (nx, ny), final_position, n - 1, dp)

    dp[key] = total
    return total