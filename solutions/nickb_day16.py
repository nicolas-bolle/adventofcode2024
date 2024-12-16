"""Day 16

networkx made things much easier, noting that:
- "Nodes" in this problem are tuples (i, j, di, dj) giving a tile and orientation (N/S/E/W)
- For networkx you need to give them names, so I went with ints as the "vertex names"
- So instead of 1 end location, there are really 4: the end tile, with each of the 4 orientations

For part 2, having networkx list out all shortest paths from one node to another is really slow
The speedup is using this way of ID-ing whether node is on the shortest path between two nodes:
- Name the nodes n, s, e for the node we care about and the start/end nodes
- Let Dse, Dsn, Dne be the shortest distance between the pairs of nodes (fast to compute)
- Then n is on the shortest path between s and e iff Dsn + Dne = Dse

(Not necessary, but note that distances in this problem are symmetric)
"""

# pylint: disable=invalid-name, redefined-outer-name

import numpy as np
import networkx as nx

from utils.inputs import get_input

DAY = 16


def parse_input_to_array(s: str) -> np.ndarray:
    """Parse input into an array"""
    return np.array([list(line) for line in s.split("\n")])


def parse_array_to_graph(A: np.ndarray) -> tuple[dict, nx.Graph, dict]:
    """Parse array into a networkx graph, along with dictionaries to convert between my node/vertex names
    Node name: (i, j, di, dj)
    Vertex name: int label
    The first dictionary says how to turn nodes into vertices, the second how to reverse that
    """
    n, m = A.shape

    # dictionary with keys the nodes (i, j, di, dj) and values their int vertex labels
    node_to_vertex = {}
    k = 0
    for i in range(n):
        for j in range(m):
            if A[i, j] == "#":
                continue
            for di, dj in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                node_to_vertex[(i, j, di, dj)] = k
                k += 1

    # inverse dict
    vertex_to_node = {vertex: node for node, vertex in node_to_vertex.items()}

    # figure out the edges
    edges_small = []
    edges_big = []
    for vertex, (i, j, di, dj) in vertex_to_node.items():
        # iterate through neighbors
        for _di, _dj in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            if _di == di and _dj == dj:
                _i, _j = i + di, j + dj
                if (_i, _j, _di, _dj) in node_to_vertex:
                    _vertex = node_to_vertex[(_i, _j, _di, _dj)]
                    edges_small.append((vertex, _vertex))
            else:
                _i, _j = i, j
                if (_i, _j, _di, _dj) in node_to_vertex:
                    _vertex = node_to_vertex[(_i, _j, _di, _dj)]
                    edges_big.append((vertex, _vertex))

    # create the graph
    G = nx.Graph()
    G.add_nodes_from(vertex_to_node.keys())
    G.add_edges_from(edges_small, weight=1)
    G.add_edges_from(edges_big, weight=1_000)

    return node_to_vertex, G, vertex_to_node


def find_i_j(A: np.ndarray, target: str) -> tuple[int]:
    """Returns the first (i, j) such that A[i, j] = target"""
    return (int(t) for t in next(zip(*np.where(A == target))))


def solution_part1(s: str) -> int:
    """Part 1 solution from the plaintext input"""
    # parsing
    A = parse_input_to_array(s)
    node_to_vertex, G, vertex_to_node = parse_array_to_graph(A)

    # identify the start/end locations
    i_start, j_start = find_i_j(A, "S")
    i_end, j_end = find_i_j(A, "E")
    di_start, dj_start = 0, 1
    vertex_start = node_to_vertex[(i_start, j_start, di_start, dj_start)]

    # measure the score for each orientation at the end location (which represent different nodes)
    # pick the best score of the four end orientations
    best_score = np.inf
    for di_end, dj_end in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        vertex_end = node_to_vertex[(i_end, j_end, di_end, dj_end)]
        score = nx.shortest_path_length(
            G, source=vertex_start, target=vertex_end, weight="weight"
        )
        best_score = min(best_score, score)

    return best_score


def solution_part2(s: str) -> int:
    """Part 2 solution from the plaintext input"""
    A = parse_input_to_array(s)
    node_to_vertex, G, vertex_to_node = parse_array_to_graph(A)

    i_start, j_start = find_i_j(A, "S")
    i_end, j_end = find_i_j(A, "E")
    di_start, dj_start = 0, 1
    vertex_start = node_to_vertex[(i_start, j_start, di_start, dj_start)]

    # similar to part 1, but just identify which end orientation gives the shortest path
    best_score = np.inf
    best_vertex_end = None
    for di_end, dj_end in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        vertex_end = node_to_vertex[(i_end, j_end, di_end, dj_end)]
        score = nx.shortest_path_length(
            G, source=vertex_start, target=vertex_end, weight="weight"
        )
        if score < best_score:
            best_score = score
            best_vertex_end = vertex_end

    # compute path lengths from the start/end nodes to everything
    scores_from_start_dict = nx.shortest_path_length(
        G, source=vertex_start, weight="weight"
    )
    scores_from_end_dict = nx.shortest_path_length(
        G, target=best_vertex_end, weight="weight"
    )

    # translate to a list of distances for each vertex
    vertices = list(vertex_to_node.keys())
    scores_from_start = [scores_from_start_dict[vertex] for vertex in vertices]
    scores_from_end = [scores_from_end_dict[vertex] for vertex in vertices]

    # extract the vertices/nodes/tiles on shortest paths
    best_vertices = np.array(vertices)[
        (np.array(scores_from_start) + np.array(scores_from_end)) == best_score
    ]
    best_nodes = [vertex_to_node[vertex] for vertex in best_vertices]
    best_tiles = list({(i, j) for i, j, _, _ in best_nodes})

    return len(best_tiles)


if __name__ == "__main__":
    s = get_input(DAY)
    print()
    soln1 = solution_part1(s)
    print("Part 1 solution:")
    print(soln1)
    print()
    soln2 = solution_part2(s)
    print("Part 2 solution:")
    print(soln2)
    print()
    print("Done")
