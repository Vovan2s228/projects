def TSP(adj_list):
    """
    Implement an algorithm that solves the Travelling Salesman Problem using backtracking. 

    :param adj_list: An adjacency list of a fully connected, undirected graph, 
    with nodes from 0 to n. 
    :type adj_list: dict(dict(int))
 
    :return: A tuple (path, cost), where path is a list with the path of 
    minimal weight, starting and ending at node 0
    :rtype: tuple(list, int)
    """
    
    best_dist = float("inf")
    best_path = []
    start_node = list(adj_list.keys())[0]
    path = [start_node]
    dist = 0

    if len(adj_list) == 1:
        return path, dist
    
    def bct(adj_list, dist, path):
        nonlocal best_dist
        nonlocal best_path

        if len(path) == len(adj_list):
            if path[0] in adj_list.get(path[-1]):
                total_dist = dist + adj_list[path[-1]][path[0]]
                if total_dist < best_dist:
                    best_dist = total_dist
                    best_path = path[:] + [path[0]]
            return
        
        for neighbor in adj_list[path[-1]]:
            if neighbor not in path:
                path.append(neighbor)
                dist += adj_list[path[-2]][neighbor]

                if dist < best_dist:
                    bct(adj_list, dist, path)

                path.pop()
                if len(path) > 0:
                    dist -= adj_list[path[-1]][neighbor]

    bct(adj_list, dist, path)
    return best_path, best_dist