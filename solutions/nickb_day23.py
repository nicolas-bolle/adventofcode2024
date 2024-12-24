"""Day 23

networkx is doing most of the work, especially for part 2
"""

# pylint: disable=invalid-name, redefined-outer-name

import networkx as nx

from utils.inputs import get_input

DAY = 23


def parse_input(s: str) -> nx.Graph:
    """Parse the input into a networkx graph"""
    return nx.from_edgelist([line.split("-") for line in s.split("\n")])


def solution_part1(s: str) -> int:
    """Part 1 solution from the plaintext input"""
    # parse input into a networkx Graph
    G = parse_input(s)

    # all the nodes that start with a 't'
    nodes_t = [node for node in G.nodes if node.startswith("t")]

    # iterate through to count triangles they're in
    # use a set so we don't double count
    triangles = set()
    for node in nodes_t:
        # look at the neighbors of the 't' node
        G_neighbors = G.subgraph(G.neighbors(node))

        # find all connected pairs
        pairs = [
            clique
            for clique in nx.enumerate_all_cliques(G_neighbors)
            if len(clique) == 2
        ]

        # those pairs along with the 't' node form a triangle
        _triangles = [tuple(sorted(pair + [node])) for pair in pairs]
        triangles.update(_triangles)

    # count the number of triangles
    num_triangles = len(triangles)

    return num_triangles


def solution_part2(s: str) -> int:
    """Part 2 solution from the plaintext input"""
    G = parse_input(s)

    # cliques that are maximal (not contained in a bigger clique)
    maximal_cliques = list(nx.algorithms.clique.find_cliques(G))

    # get the largest of these
    max_size = max(len(clique) for clique in maximal_cliques)
    largest_cliques = [clique for clique in maximal_cliques if len(clique) == max_size]

    # there's just one
    assert len(largest_cliques) == 1
    clique = largest_cliques[0]

    # turn it into the password
    password = ",".join(sorted(clique))

    return password


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
