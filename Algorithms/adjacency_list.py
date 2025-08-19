import numpy as np
import typing


class AdjacencyList(object):

    @staticmethod
    def count_vertices_undirected_graph(
            adj_list: typing.Dict[int, typing.List[int]]) -> int:
        """
        Counts the number of vertices in an undirected graph

        :param adj_list: The graph in adjacency list format, where
        adj_list[i] consists of a list, where each element of that list
        indicates an edge to a specific vertex
        :return: int, the number of vertices
        """
        return len(adj_list)

    @staticmethod
    def count_edges_undirected_graph(
            adj_list: typing.Dict[int, typing.List[int]]) -> int:
        """
        Counts the number of edges in an undirected graph

        :param adj_list: The graph in adjacency list format, where
        adj_list[i] consists of a list, where each element of that list
        indicates an edge to a specific vertex
        :return: int, the number of edges
        """
        n_edges = 0
        for i in adj_list:
            for j in adj_list[i]:
                n_edges +=1
        n_edges /= 2

        return n_edges

    @staticmethod
    def count_vertices_directed_graph(
            adj_list: typing.Dict[int, typing.List[int]]) -> int:
        """
        Counts the number of vertices in a directed graph

        :param adj_list: The graph in adjacency list format, where
        adj_list[i] consists of a list, where each element of that list
        indicates an edge to a specific vertex
        :return: int, the number of vertices
        """
        return len(adj_list)

    @staticmethod
    def count_edges_directed_graph(
            adj_list: typing.Dict[int, typing.List[int]]) -> int:
        """
        Counts the number of edges in an undirected graph

        :param adj_list: The graph in adjacency list format, where
        adj_list[i] consists of a list, where each element of that list
        indicates an edge to a specific vertex
        :return: int, the number of nodes/vertices
        """
        n_edges = 0
        for i in adj_list:
            for j in adj_list[i]:
                n_edges +=1

        return n_edges

    @staticmethod
    def count_odd_neighbours_undirected_graph(
            adj_list: typing.Dict[int, typing.List[int]]) -> int:
        """
        Counts the number of vertices that have an odd number of neighbours

        :param adj_list: The graph in adjacency list format, where
        adj_list[i] consists of a list, where each element of that list
        indicates an edge to a specific vertex
        :return: int, the number of edges
        """
        n_odd_vert = 0
        for i in adj_list:
            if len(adj_list[i]) % 2 != 0:
                n_odd_vert += 1
        
        return n_odd_vert


    @staticmethod
    def list_to_matrix(
            adj_list: typing.Dict[int, typing.List[int]]) -> np.array:
        """
        Accepts a graph in the adjacency list format, and returns it in the
        adjacency matrix format.

        :param adj_list: The graph in adjacency list format, where
        adj_list[i] consists of a list, where each element of that list
        indicates an edge to a specific vertex
        :return: The graph in adjacency matrix format, where
        adj_matrix[i][j] indicates whether there is an edge between vertex i
        and j
        """
        n = len(adj_list)
        matrix = np.zeros((n, n), dtype = int)
        for i in adj_list:
            for j in adj_list[i]:
                matrix[i][j] = 1
        
        return matrix
