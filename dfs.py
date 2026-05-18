"""
PacketPath DFS module.

This module uses recursive Depth-First Search (DFS) to map all substations
reachable from a fault node in the PacketPath substation graph.
"""

from graph import create_packetpath_graph


def recursive_dfs(graph, current_node, visited, traversal_order):
    """
    Recursively visit all substations reachable from current_node.

    Time Complexity: O(V + E), where V is the number of substations and E is
    the number of packet links.
    Space Complexity: O(V), for the visited set, traversal order, and recursive
    call stack in the worst case.

    Args:
        graph (Graph): PacketPath graph object with an adjacency_list attribute.
        current_node (str): Current substation being explored.
        visited (set[str]): Substations already visited by DFS.
        traversal_order (list[str]): Ordered list of visited substations.
    """
    visited.add(current_node)
    traversal_order.append(current_node)

    for neighbor in graph.adjacency_list[current_node]:
        if neighbor not in visited:
            recursive_dfs(graph, neighbor, visited, traversal_order)


def find_affected_substations(graph, fault_node):
    """
    Find all affected substations reachable from a fault node using DFS.

    Args:
        graph (Graph): PacketPath graph object with an adjacency_list attribute.
        fault_node (str): Substation where the fault starts.

    Returns:
        tuple[set[str], list[str]]: Affected substations and DFS traversal order.
    """
    if fault_node not in graph.adjacency_list:
        raise ValueError(f"Fault node not found in graph: {fault_node}")

    visited = set()
    traversal_order = []

    recursive_dfs(graph, fault_node, visited, traversal_order)

    return visited, traversal_order


def display_dfs_result(fault_node, affected_zones, traversal_order):
    """
    Display affected zones and DFS traversal order.

    Args:
        fault_node (str): Starting fault substation.
        affected_zones (set[str]): All substations reachable from the fault node.
        traversal_order (list[str]): DFS node visit order.
    """
    print("PacketPath DFS Affected Zone Mapper")
    print("=" * 36)
    print(f"Fault Node: {fault_node}")
    print()

    print("Affected Zones:")
    for zone_number, substation in enumerate(traversal_order, start=1):
        print(f"{zone_number}. {substation}")
    print(f"Total Affected Substations: {len(affected_zones)}")
    print()

    print("DFS Traversal Order:")
    print(" -> ".join(traversal_order))


def main():
    """Run a PacketPath DFS demo."""
    packetpath_graph = create_packetpath_graph()
    fault_node = "Central Relay Substation"

    affected_zones, traversal_order = find_affected_substations(
        packetpath_graph,
        fault_node,
    )

    display_dfs_result(fault_node, affected_zones, traversal_order)


if __name__ == "__main__":
    main()