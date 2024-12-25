"""Day 24

Part 1: I made Gate objects to organize things

Part 2: this was a pain
After a bunch of trial and error I ended up just manually finding the swaps
    by visualizing things as a graph
The details of what I did in a notebook are below in solution_part2()
I did a quick "addition sanity check" via g() to find the areas where the swaps were
And then drew the graph to manually look through the gates for what was wrong
The full circuit is just 1 half adder and 44 full adders
And the full adders follow this 5 gate implementation:
https://en.wikipedia.org/wiki/Adder_(electronics)#Full_adder

I don't think there's a good automatic solution?
Since I think you'd have to assume you know how they implemented the addition,
    and specifically how they implemented full adders
Like, I could imagine a cool spectral solution where you look for a permutation matrix
    to match the current adjacency matrix's spectrum to that of a  "target" adjacency matrix
But that requires knowing exactly what the form of the target circuit is
"""

# pylint: disable=invalid-name, redefined-outer-name

from abc import ABC, abstractmethod
from typing import Self

import numpy as np
import networkx as nx

from utils.inputs import get_input

DAY = 24


class Gate(ABC):
    """A logic gate that can be called to get its value"""

    name: str

    input_gate_1: Self
    input_gate_2: Self

    value: bool

    def __init__(self, name: str, input_gate_1: Self = None, input_gate_2: Self = None):
        self.name = name
        self.input_gate_1 = input_gate_1
        self.input_gate_2 = input_gate_2
        self.value = None

    @property
    def input_gates(self):
        return {self.input_gate_1.name, self.input_gate_2.name}

    def __lt__(self, other_gate):
        return self.name < other_gate.name

    def __call__(self) -> bool:
        if self.value is None:
            self.value = self._call()
        return self.value

    def reset(self):
        self.value = None

    @abstractmethod
    def _call(self) -> bool:
        """Return the value of the gate"""
        return True


class GateAnd(Gate):
    """AND gate"""

    def _call(self) -> bool:
        """Return the value of the gate"""
        return self.input_gate_1() and self.input_gate_2()


class GateOr(Gate):
    """OR gate"""

    def _call(self) -> bool:
        """Return the value of the gate"""
        return self.input_gate_1() or self.input_gate_2()


class GateXor(Gate):
    """XOR gate"""

    def _call(self) -> bool:
        """Return the value of the gate"""
        return self.input_gate_1() ^ self.input_gate_2()


class GateValue(Gate):
    """Not really a gate, just a node holding a value"""

    def __init__(self, name: str, value: bool):
        super().__init__(name=name, input_gate_1=None, input_gate_2=None)
        self.value = value

    def reset(self):
        pass

    def _call(self) -> bool:
        """Return the value of the gate"""
        return self.value


def get_gates(s) -> list[Gate]:
    """Parse the input into a list of (connected) gate objects"""
    gate_value_lines, gate_lines = tuple(s.strip().split("\n\n"))
    gates1 = [parse_gate_value_line(line) for line in gate_value_lines.split("\n")]
    gates2 = [parse_gate_line(line) for line in gate_lines.split("\n")]
    gates_dict = {gate.name: gate for gate in gates1 + gates2}
    gates = list(gates_dict.values())
    for gate in gates:
        if isinstance(gate.input_gate_1, str):
            gate.input_gate_1 = gates_dict[gate.input_gate_1]
        if isinstance(gate.input_gate_2, str):
            gate.input_gate_2 = gates_dict[gate.input_gate_2]
    return gates


def parse_gate_value_line(line: str) -> GateValue:
    """Parse a "value" gate into an object"""
    a, b = tuple(line.split(": "))
    return GateValue(name=a, value=bool(int(b)))


def parse_gate_line(line: str) -> Gate:
    """Parse a "real" gate into an object
    Its input gates are just strings for now (will be fixed in get_gates())
    """
    a, b, c, _, d = tuple(line.split(" "))
    match b:
        case "AND":
            t = GateAnd
        case "OR":
            t = GateOr
        case "XOR":
            t = GateXor
        case _:
            raise Exception(f"Unknown gate {b}")
    return t(name=d, input_gate_1=a, input_gate_2=c)


def find_input_gates(gates: list[Gate]) -> tuple[list[Gate], list[Gate]]:
    """Find all input x and y gates"""
    x_gates = []
    y_gates = []
    for gate in gates:
        if gate.name[0] == "x":
            x_gates.append(gate)
        if gate.name[0] == "y":
            y_gates.append(gate)
    x_gates = sorted(x_gates)
    y_gates = sorted(y_gates)
    return x_gates, y_gates


def find_output_gates(gates: list[Gate]) -> list[Gate]:
    """Find all output z gates"""
    z_gates = []
    for gate in gates:
        if gate.name[0] == "z":
            z_gates.append(gate)
    z_gates = sorted(z_gates)
    return z_gates


def f(
    gates: list[Gate],
    x_gates: list[GateValue],
    y_gates: list[GateValue],
    z_gates: list[Gate],
    x: list[bool],
    y: list[bool],
):
    """Given a setup of gates and a list of bool values for the x and y gates to take,
    return the bool values of the z gates
    """
    x = list(x)
    y = list(y)

    assert len(x) == len(x_gates)
    assert len(y) == len(y_gates)

    for gate, value in zip(x_gates + y_gates, x + y):
        gate.value = value

    for gate in gates:
        gate.reset()

    z = [gate() for gate in z_gates]

    return z


def g(
    gates: list[Gate],
    x_gates: list[GateValue],
    y_gates: list[GateValue],
    z_gates: list[Gate],
    i: int,
) -> float:
    """Tries adding 2**i and 2**i to see if we get 2**(i+1)"""
    x = [False] * len(x_gates)
    y = [False] * len(y_gates)
    x[i] = True
    y[i] = True
    z = f(gates, x_gates, y_gates, z_gates, x, y)
    num = int("".join([str(int(x)) for x in reversed(z)]), base=2)
    return float(np.log2(num))


def get_gate_node_name(gate: Gate):
    """A name for a gate as a node of a graph"""
    return gate.name + type(gate).__name__[4:]


def draw_subgraph(
    G: nx.DiGraph,
    I: list[int],
    r=3,
    k=20,
    iterations=20,
):
    """Draw the part of the graph around the value nodes given by I"""
    # get node names
    names = []
    for i in I:
        name = f"x{str(i).rjust(2, '0')}Value"
        names.append(name)
        name = f"y{str(i).rjust(2, '0')}Value"
        names.append(name)

    # form the relevant subgraph
    nodes = set()
    for name in names:
        nodes = nodes | set(nx.ego_graph(G, name, radius=r).nodes)
    _G = nx.induced_subgraph(G, nodes)

    # draw it
    pos = nx.spectral_layout(_G)
    pos = nx.spring_layout(_G, pos=pos, k=k, iterations=iterations)
    nx.draw(_G, pos=pos, with_labels=True)


def solution_part1(s: str) -> int:
    """Part 1 solution from the plaintext input"""
    gates = get_gates(s)
    z_gates = find_output_gates(gates)
    z = [gate() for gate in z_gates]
    z_num = int("".join([str(int(x)) for x in reversed(z)]), base=2)
    return z_num


def solution_part2(s: str) -> str:
    """Part 2 solution from the plaintext input"""
    # pylint: disable=pointless-string-statement
    """
    # doing the 4 swaps
    s_prime = (
        s.replace("-> z14", "$swap")
        .replace("-> qbw", "-> z14")
        .replace("$swap", "-> qbw")
        .replace("-> z34", "$swap")
        .replace("-> wcb", "-> z34")
        .replace("$swap", "-> wcb")
        .replace("-> wjb", "$swap")
        .replace("-> cvp", "-> wjb")
        .replace("$swap", "-> cvp")
        .replace("-> mkk", "$swap")
        .replace("-> z10", "-> mkk")
        .replace("$swap", "-> z10")
    )

    # parse into gates
    gates = get_gates(s_prime)
    x_gates, y_gates = find_input_gates(gates)
    z_gates = find_output_gates(gates)

    # print out i for which 2**i + 2**i is not computed as 2**(i+1)
    # i.e. the parts of the circuit that definitely have issues
    for i in range(len(x_gates)):
        j = g(gates, x_gates, y_gates, z_gates, i)
        if j != i + 1:
            print(i)
            print(j)
            print()

    # parse into a graph
    G = nx.DiGraph()
    for gate in gates:
        if isinstance(gate, GateValue):
            G.add_node(get_gate_node_name(gate))
        else:
            G.add_edge(get_gate_node_name(gate), get_gate_node_name(gate))
            G.add_edge(get_gate_node_name(gate), get_gate_node_name(gate))

    # draw the problem areas for manual investigation
    draw_subgraph(G, [13, 14, 15])
    draw_subgraph(G, [33, 34, 35])
    draw_subgraph(G, [25, 26])
    draw_subgraph(G, [9, 10, 11])
    """

    # the solution from the nodes involved in the swaps
    soln = ",".join(sorted("z14, qbw, z34, wcb, wjb, cvp, mkk, z10".split(", ")))

    return soln


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
