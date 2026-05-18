"""
PacketPath graph module.

This module provides a simple adjacency-list graph for modelling packet paths
between electrical substations. It includes a reusable Graph class and a small
demo network with 20 sample substations.
"""


class Graph:
    """Adjacency-list graph implementation for PacketPath."""

    def __init__(self, directed=False):
        """
        Initialize an empty graph.

        Args:
            directed (bool): If True, edges are one-way. If False, edges are
                added in both directions.
        """
        self.directed = directed
        self.adjacency_list = {}

    def add_node(self, node):
        """
        Add a node to the graph if it does not already exist.

        Args:
            node (str): Name of the substation/node.
        """
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []

    def add_edge(self, source, destination):
        """
        Add an edge between two nodes.

        Missing nodes are created automatically.

        Args:
            source (str): Starting node for the edge.
            destination (str): Ending node for the edge.
        """
        self.add_node(source)
        self.add_node(destination)

        if destination not in self.adjacency_list[source]:
            self.adjacency_list[source].append(destination)

        if not self.directed and source not in self.adjacency_list[destination]:
            self.adjacency_list[destination].append(source)

    def display_graph(self):
        """Display the graph as an adjacency list."""
        for node, neighbors in self.adjacency_list.items():
            connections = ", ".join(neighbors) if neighbors else "No connections"
            print(f"{node} -> {connections}")


def create_packetpath_graph():
    """
    Create and return a PacketPath graph with 20 sample substations.

    Returns:
        Graph: A sample substation network graph.
    """
    graph = Graph()

    substations = [
        "North Grid Substation",
        "South Grid Substation",
        "East Grid Substation",
        "West Grid Substation",
        "Central Relay Substation",
        "Riverbend Substation",
        "Hilltop Substation",
        "Lakeside Substation",
        "Industrial Park Substation",
        "Airport Substation",
        "Metro Core Substation",
        "Greenfield Substation",
        "Old Town Substation",
        "Harbor Substation",
        "University Substation",
        "Medical District Substation",
        "Tech Park Substation",
        "Solar Farm Substation",
        "Wind Ridge Substation",
        "Backup Control Substation",
    ]

    for substation in substations:
        graph.add_node(substation)

    sample_edges = [
        ("Central Relay Substation", "North Grid Substation"),
        ("Central Relay Substation", "South Grid Substation"),
        ("Central Relay Substation", "East Grid Substation"),
        ("Central Relay Substation", "West Grid Substation"),
        ("North Grid Substation", "Hilltop Substation"),
        ("North Grid Substation", "Wind Ridge Substation"),
        ("South Grid Substation", "Industrial Park Substation"),
        ("South Grid Substation", "Airport Substation"),
        ("East Grid Substation", "Riverbend Substation"),
        ("East Grid Substation", "Lakeside Substation"),
        ("West Grid Substation", "Old Town Substation"),
        ("West Grid Substation", "Harbor Substation"),
        ("Metro Core Substation", "University Substation"),
        ("Metro Core Substation", "Medical District Substation"),
        ("Metro Core Substation", "Tech Park Substation"),
        ("Greenfield Substation", "Solar Farm Substation"),
        ("Greenfield Substation", "Wind Ridge Substation"),
        ("Backup Control Substation", "Central Relay Substation"),
        ("Backup Control Substation", "Metro Core Substation"),
        ("Tech Park Substation", "Industrial Park Substation"),
        ("Medical District Substation", "Old Town Substation"),
        ("Harbor Substation", "Airport Substation"),
    ]

    for source, destination in sample_edges:
        graph.add_edge(source, destination)

    return graph


def main():
    """Run a sample PacketPath graph demo."""
    packetpath_graph = create_packetpath_graph()
    print("PacketPath Substation Graph")
    print("=" * 28)
    packetpath_graph.display_graph()


if __name__ == "__main__":
    main()