from collections import defaultdict
from helpers import readdaylines, profiler
from itertools import combinations
import networkx as nx

lines = readdaylines(23, 2024, example=False)
graph = defaultdict(list)
for edge in lines:
    v1, v2 = edge.split("-")
    graph[v1].append(v2)
    graph[v2].append(v1)

def cliques(graph, size=3):
    for nodes in combinations(graph.keys(), size):
        if all(v2 in graph[v1] for i, v1 in enumerate(nodes) for v2 in nodes[i + 1:]):
            yield nodes

@profiler
def part1():
    return sum(any(v.startswith("t") for v in clique)
               for clique in cliques(graph, size=3))

@profiler
def part2():
    G = nx.Graph()
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
    print(G)

    cliques = nx.find_cliques(G)
    mx = max(cliques, key=len)
    mx.sort()
    return ",".join(mx)
