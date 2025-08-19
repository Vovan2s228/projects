from collections import defaultdict

class UnionFind:
    def __init__(self):
        self.parent = {}
        self.rank = {}

    def find(self, x: str) -> str:
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
            return x
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: str, y: str) -> bool:
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False

        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_y] < self.rank[root_x]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        return True


def kruskal(adj_list: dict[str, list[tuple[str, int]]]) -> tuple[int, dict[str, list[tuple[str, int]]]]:
    edges = set()
    for u in adj_list:
        for v, w in adj_list[u]:
            if (v, u, w) not in edges:
                edges.add((u, v, w))

    sorted_edges = sorted(edges, key=lambda x: x[2])

    uf = UnionFind()
    mst_adj_list = defaultdict(list)
    total_weight = 0

    for u, v, w in sorted_edges:
        if uf.union(u, v):
            mst_adj_list[u].append((v, w))
            mst_adj_list[v].append((u, w))
            total_weight += w

    return total_weight, dict(mst_adj_list)
