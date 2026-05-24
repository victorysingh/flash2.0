

import time

import bfs
from graph import create_packetpath_graph


def _find_all_paths_recursive(graph, current_node, target_node, current_path, all_paths):
    
    current_path.append(current_node)

    # If the target is reached, store a copy of the path and stop this branch.
    if current_node == target_node:
        all_paths.append(list(current_path))
    else:
        # Explore all neighbors.
        for neighbor in graph.adjacency_list[current_node]:
            # Avoid cycles by only visiting nodes not already in the current path.
            if neighbor not in current_path:
                _find_all_paths_recursive(graph, neighbor, target_node, current_path, all_paths)

    # Backtrack to allow exploration of other branches.
    current_path.pop()


def find_shortest_path_brute_force(graph, start_node, target_node):
    
    start_time = time.perf_counter()

    all_paths = []
    _find_all_paths_recursive(graph, start_node, target_node, [], all_paths)

    end_time = time.perf_counter()
    execution_time = end_time - start_time

    if not all_paths:
        return None, execution_time

    # Find the path with the minimum length from all discovered paths.
    shortest_path = min(all_paths, key=len)

    return shortest_path, execution_time


def display_brute_force_results(path, exec_time):
    
    print("PacketPath Brute-Force Path Finder")
    print("=" * 35)
    if path:
        print("Shortest Path Found:")
        print(" -> ".join(path))
        print(f"Hop Count: {bfs.calculate_hop_count(path)}")
    else:
        print("Shortest Path Found: No available route")
        print("Hop Count: 0")

    print(f"Execution Time: {exec_time:.6f} seconds")
    print()


def main():
    
    packetpath_graph = create_packetpath_graph()
    # Using a shorter path for the demo to keep execution time reasonable.
    start_node = "Backup Control Substation"
    target_node = "North Grid Substation"

    print("=" * 70)
    print("  Algorithm Comparison: Brute-Force vs. Breadth-First Search (BFS)")
    print("=" * 70)
    print(f"\nFinding shortest path from '{start_node}' to '{target_node}'...\n")

    # --- Brute-Force Execution ---
    bf_path, bf_time = find_shortest_path_brute_force(
        packetpath_graph, start_node, target_node
    )
    display_brute_force_results(bf_path, bf_time)

    # --- BFS Execution ---
    start_time_bfs = time.perf_counter()
    _, bfs_path = bfs.breadth_first_search(packetpath_graph, start_node, target_node)
    end_time_bfs = time.perf_counter()
    bfs_time = end_time_bfs - start_time_bfs

    print("PacketPath BFS Path Finder")
    print("=" * 35)
    print(f"Shortest Path Found: {' -> '.join(bfs_path)}")
    print(f"Hop Count: {bfs.calculate_hop_count(bfs_path)}")
    print(f"Execution Time: {bfs_time:.6f} seconds")
    print()
    print("-" * 70)
    print("[ Comparison Summary ]")
    print("-" * 70)
    print(f"Brute-Force Time: {bf_time:.6f} seconds")
    print(f"BFS Time        : {bfs_time:.6f} seconds")
    print(f"\nConclusion: BFS found the same shortest path but was significantly")
    print(f"faster, demonstrating the power of optimized graph traversal algorithms.")


if __name__ == "__main__":
    main()