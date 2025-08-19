def dijkstra(start: str, adj_list: dict[str, list[tuple[str, int]]]) -> tuple[dict[str, int], dict[str, str]]:
    """Implement Dijkstra's algorithm to find the shortest path from the start to every other vertex in the graph.

	For example input, please review the public tests on Brightspace. 

    :param start: A string containing the name of the vertex where you start from.
    :type start: str
    :param adj_list: An adjacency list for a weighted graph. It is a dictionary where 
        the keys are vertices and the values are lists of tuples of the form (vertex, weight) 
        where weight is the weight of the edge from the key vertex to the value vertex.
    :type adj_list: dict[str, tuple[str, int]]
    :return: Returns a tuple (distances, history) where distances is a dictionary where 
        the values are the minimum cost to get from the start to the keys.
        The cost is the sum of the weights of the edges in the path. 
        History is a dictionary where each item states that 
        the last edge in the minimal path to the key was from the value to the key.
    :rtype: tuple[dict[str, int], dict[str, str]]
    """

    distances = {node: float('inf') for node in adj_list}
    distances[start] = 0

    history = {}
    visited = set()
    history[start] = None

    while len(visited) < len(adj_list):
        min_node = None
        min_dist = float('inf')
        for node in adj_list:
            if node not in visited and distances[node] < min_dist:
                min_node = node
                min_dist = distances[node]

        if min_node is None:
            break

        visited.add(min_node)

        for neighbor, weight in adj_list[min_node]:
            if neighbor not in visited:
                new_dist = distances[min_node] + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    history[neighbor] = min_node

    return distances, history
        
    
def get_path(goal: str, history: dict[str]) -> list[str]:
    """Given the history returned by the dijkstra function and a vertex goal
        return a minimum path from the start to the goal.

    :param goal: The returned path must go from the start to the goal vertex.
    :type goal: str
    :param history: The history that is returned by the dijkstra function.
    :type history: dict[str]
    :return: A path from the start vertex to the goal vertex.
    :rtype: list[str]
    """
    path = []
    current = goal

    while current in history:
        path.append(current)
        current = history.get(current)
    
    path.reverse()
    return path
