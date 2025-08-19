
"""
In this assignment, you will create recursively all hamiltonian cycles for any fully connected graph.
A Hamiltonian cycle is a cycle in a graph that visits each node exactly once
(not to be confused with an Eulerian cycle), see also lecture 2 and lecture 5.

Note 1: that the list can be represented by the order of n nodes,
but that the first node does not need to be repeated in the list (as this is implicit).
Of course, the sequence of nodes is only a valid Hamiltonian path,
if one can return from the last node to the first node.

Note 2: You are not allowed to use any modules/packages that return the answer in one step such as itertools.

Note 3: find_hamiltonian_cycles_helper is an optional helper function and does not need to be implemented.

Hint: find_hamiltonian_cycles is hard to make recursive. So, it might be easier to use one or more helper functions.
      To give you an idea for a recursive function that is easier to implement you can use find_hamiltonian_cycles_helper.
"""

def find_hamiltonian_cycles(adj_list, start_node):
    """
    Calculates all Hamiltonian cycles in a fully connected graph based on the adjacency list, starting from a specific node.

    A Hamiltonian cycle is a cycle that visits each node exactly once and returns to the starting node.

    :param adj_list: A dictionary representing the adjacency list of the graph, where keys are nodes
                     and values are dictionaries of neighboring nodes with edge weights.
    :type adj_list: dict[object, dict[object, int]]
    :param start_node: The node from which the Hamiltonian cycle should start.
    :type start_node: object
    :return: A list of all Hamiltonian cycles, where each cycle is represented as a list of nodes.
    :rtype: list[list[object]]
    """
    
    all_nodes = list(adj_list.keys())
    all_nodes.remove(start_node)
    possible_paths = find_hamiltonian_cycles_helper(all_nodes)
    valid_cycles = []
    for perm in possible_paths:
        cycle = [start_node] + perm
        is_valid = True
        for i in range(len(cycle) - 1):
            current_node = cycle[i]
            next_node = cycle[i + 1]
            if next_node not in adj_list[current_node]:
                is_valid = False
                break
        if cycle[-1] not in adj_list or start_node not in adj_list[cycle[-1]]:
            is_valid = False
        if is_valid:
            valid_cycles.append(cycle)
    return valid_cycles

def find_hamiltonian_cycles_helper(nodes):
    """
    Recursively generates all Hamiltonian cycles by permuting the given list of nodes.

    :param nodes: The list of nodes in the graph, excluding the starting node.
    :type nodes: list[object]
    :return: A list of all Hamiltonian cycles, where each cycle is represented as a list of nodes.
    :rtype: list[list[object]]
    """

    if len(nodes) <= 1:
        return [nodes]
    permutations = []
    for i in range(len(nodes)):
        current = nodes[i]
        rest = nodes[:i] + nodes[i+1:]
        sub_permutations = find_hamiltonian_cycles_helper(rest)
        for sub_perm in sub_permutations:
            permutations.append([current] + sub_perm)
    return permutations

    
if __name__ == "__main__":
    adj_list = {
        'A': {'B': 4, 'C': 6},
        'B': {'A': 4, 'C': 5},
        'C': {'A': 6, 'B': 5}
    }
    print(find_hamiltonian_cycles(adj_list, start_node='A'))
