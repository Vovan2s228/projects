def maze_solver(maze):
    """
    Starting in the top left corner (0,0) determine whether there is a path,
    moving horizontally and vertically, to exit the labyrinth in the bottom-right corner.

    :para maze: A 2D list representing a maze, with 0 for paths and 1 for walls
    :type maze: list[list[int]]

    :return: True/False whether there is a way to exit the labyrinth
    """
    
    pos = (0, 0)
    visited = set()
    visited.add((0, 0))

    def bct(maze, pos):
        if pos == (len(maze) - 1, len(maze[0]) - 1):
            return True
        
        if pos[0] + 1 < len(maze) and maze[pos[0] + 1][pos[1]] == 0 and (pos[0] + 1, pos[1]) not in visited:
            new_pos = (pos[0]+1, pos[1])
            visited.add(new_pos)
            if bct(maze, new_pos):
                return True
        if pos[0] - 1 >= 0 and maze[pos[0] - 1][pos[1]] == 0 and (pos[0] - 1, pos[1]) not in visited:
            new_pos = (pos[0]-1, pos[1])
            visited.add(new_pos)
            if bct(maze, new_pos):
                return True
        if pos[1] + 1 < len(maze[0]) and maze[pos[0]][pos[1] + 1] == 0 and (pos[0], pos[1] + 1) not in visited:
            new_pos = (pos[0], pos[1]+1)
            visited.add(new_pos)
            if bct(maze, new_pos):
                return True
        if pos[1] - 1 >= 0 and maze[pos[0]][pos[1] - 1] == 0 and (pos[0], pos[1] - 1) not in visited:
            new_pos = (pos[0], pos[1]-1)
            visited.add(new_pos)
            if bct(maze, new_pos):
                return True
        
        return False

    return bct(maze, pos)