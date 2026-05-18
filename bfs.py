"""
PacketPath BFS module.

This module uses queue-based Breadth-First Search (BFS) to find the shortest
unweighted path between a repair depot and a fault location in the PacketPath
substation graph.
"""

from collections import deque

from graph import create_packetpath_graph


def breadth_first_search(graph, start_node, target_node):
    """
    Perform BFS and find the shortest path from start_node to target_node.

    BFS explores the graph level by level, so the first time the target is
    reached in an unweighted graph, the discovered path is the shortest path.

    Time Complexity: O(V + E), where V is the number of substations and E is
    the number of packet links.
    Space Complexity: O(V), for the queue, visited set, parent map, and
    traversal order.

    Args:
        graph (Graph): PacketPath graph object with an adjacency_list attribute.
        start_node (str): Repair depot starting substation.
        target_node (str): Fault location destination substation.

    Returns:
        tuple[list[str], list[str]]: Traversal order and shortest path.
    """
    if start_node not in graph.adjacency_list:
        raise ValueError(f"Start node not found in graph: {start_node}")

    if target_node not in graph.adjacency_list:
        raise ValueError(f"Target node not found in graph: {target_node}")

    queue = deque([start_node])
    visited = {start_node}
    parent = {start_node: None}
    traversal_order = []

    while queue:
        current_node = queue.popleft()
        traversal_order.append(current_node)

        if current_node == target_node:
            break

        for neighbor in graph.adjacency_list[current_node]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current_node
                queue.append(neighbor)

    shortest_path = reconstruct_path(parent, start_node, target_node)
    return traversal_order, shortest_path


def reconstruct_path(parent, start_node, target_node):
    """
    Reconstruct the shortest path using the BFS parent map.

    Args:
        parent (dict[str, str | None]): Map of each visited node to its parent.
        start_node (str): Repair depot starting substation.
        target_node (str): Fault location destination substation.

    Returns:
        list[str]: Shortest path from start_node to target_node, or an empty
        list if no route exists.
    """
    if target_node not in parent:
        return []

    path = []
    current_node = target_node

    while current_node is not None:
        path.append(current_node)
        current_node = parent[current_node]

    path.reverse()

    if path[0] != start_node:
        return []

    return path


def calculate_hop_count(path):
    """
    Calculate the number of hops in a path.

    Args:
        path (list[str]): Ordered path of substations.

    Returns:
        int: Number of edges between substations. Returns 0 if no path exists.
    """
    return max(len(path) - 1, 0)


def display_bfs_result(repair_depot, fault_location, traversal_order, shortest_path):
    """
    Display BFS traversal details for PacketPath.

    Args:
        repair_depot (str): Starting repair depot substation.
        fault_location (str): Target fault location substation.
        traversal_order (list[str]): BFS node visit order.
        shortest_path (list[str]): Shortest route from depot to fault location.
    """
    print("PacketPath BFS Route Finder")
    print("=" * 31)
    print(f"Repair Depot: {repair_depot}")
    print(f"Fault Location: {fault_location}")
    print()

    print("Traversal Order:")
    print(" -> ".join(traversal_order))
    print()

    if shortest_path:
        print("Shortest Path:")
        print(" -> ".join(shortest_path))
        print(f"Hop Count: {calculate_hop_count(shortest_path)}")
    else:
        print("Shortest Path: No available route")
        print("Hop Count: 0")


def main():
    """Run a PacketPath BFS demo."""
    packetpath_graph = create_packetpath_graph()

    repair_depot = "Backup Control Substation"
    fault_location = "Solar Farm Substation"

    traversal_order, shortest_path = breadth_first_search(
        packetpath_graph,
        repair_depot,
        fault_location,
    )

    display_bfs_result(
        repair_depot,
        fault_location,
        traversal_order,
        shortest_path,
    )


if __name__ == "__main__":
    main()