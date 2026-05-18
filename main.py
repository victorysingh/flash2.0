"""
PacketPath main application.

This module serves as the primary entry point and project showcase,
integrating all routing, mapping, and scheduling components into a
cohesive simulation.
"""

import time

import bfs
import brute_force
import dfs
import graph
import scheduler


def display_banner():
    """Display the main PacketPath application banner."""
    print("=" * 70)
    print(" " * 10 + "PacketPath: Power Grid Routing & Repair Simulation")
    print("=" * 70)
    print()


def display_section_separator(title):
    """
    Display a formatted section separator.

    Args:
        title (str): Section title.
    """
    print(f"\n[ {title} ]")
    print("-" * 70)


def main():
    """Run the complete PacketPath application flow."""
    # 1. Display PacketPath project banner
    display_banner()

    # 2. Load power grid graph
    display_section_separator("1. Loading Power Grid Topology")
    packetpath_graph = graph.create_packetpath_graph()
    packetpath_graph.display_graph()

    # 3. Simulate fault detection
    repair_depot = "Backup Control Substation"
    fault_node = "Solar Farm Substation"
    
    display_section_separator("2. Fault Detection Simulation")
    print(f"[!] ALERT: Fault detected at '{fault_node}'!")
    print(f"[*] Dispatching emergency assessment from '{repair_depot}'.")
    print()

    # 4. Run BFS shortest path analysis
    display_section_separator("3. BFS: Shortest Path Analysis")
    bfs_traversal, shortest_path = bfs.breadth_first_search(
        packetpath_graph, repair_depot, fault_node
    )
    bfs.display_bfs_result(repair_depot, fault_node, bfs_traversal, shortest_path)

    # 5. Run DFS affected zone mapping
    display_section_separator("4. DFS: Affected Zone Mapping")
    affected_zones, dfs_traversal = dfs.find_affected_substations(
        packetpath_graph, fault_node
    )
    dfs.display_dfs_result(fault_node, affected_zones, dfs_traversal)

    # 6. Run Round Robin repair crew scheduling
    display_section_separator("5. Round Robin: Repair Crew Scheduling")
    time_quantum = 4
    repair_crews = [
        scheduler.create_repair_crew("Crew-Alpha", 12),
        scheduler.create_repair_crew("Crew-Beta", 8),
        scheduler.create_repair_crew("Crew-Gamma", 15),
        scheduler.create_repair_crew("Crew-Delta", 6),
    ]
    
    gantt_chart = scheduler.round_robin_schedule(repair_crews, time_quantum)
    scheduler.display_schedule_summary(repair_crews, time_quantum, gantt_chart)

    # 6. Run Algorithm Performance Comparison
    display_section_separator("6. Algorithm Performance Comparison")
    # Use a shorter path for the comparison to ensure brute-force runs quickly.
    comparison_start_node = "Backup Control Substation"
    comparison_target_node = "North Grid Substation"
    print(
        f"Comparing pathfinding from '{comparison_start_node}' to "
        f"'{comparison_target_node}'...\n"
    )

    # --- Brute-Force Execution ---
    bf_path, bf_time = brute_force.find_shortest_path_brute_force(
        packetpath_graph, comparison_start_node, comparison_target_node
    )
    brute_force.display_brute_force_results(bf_path, bf_time)

    # --- BFS Execution ---
    start_time_bfs = time.perf_counter()
    _, bfs_comp_path = bfs.breadth_first_search(
        packetpath_graph, comparison_start_node, comparison_target_node
    )
    end_time_bfs = time.perf_counter()
    bfs_time = end_time_bfs - start_time_bfs

    print("PacketPath BFS Path Finder")
    print("=" * 35)
    print(f"Shortest Path Found: {' -> '.join(bfs_comp_path)}")
    print(f"Hop Count: {bfs.calculate_hop_count(bfs_comp_path)}")
    print(f"Execution Time: {bfs_time:.6f} seconds")
    print()

    # --- Comparison Summary ---
    print("-" * 70)
    print("[ Comparison Summary ]")
    print("-" * 70)
    print(f"Brute-Force Time : {bf_time:.6f} seconds")
    print(f"BFS Time         : {bfs_time:.6f} seconds")
    if bfs_time > 0 and bf_time > bfs_time:
        print(f"\nConclusion: BFS found the optimal path ~{bf_time / bfs_time:.0f}x faster.")

    # 7. Display final statistics summary
    display_section_separator("7. Final Simulation Summary")
    print(f"Network Size                  : {len(packetpath_graph.adjacency_list)} Substations")
    print(f"Fault Location                : {fault_node}")
    print(f"Distance to Fault             : {bfs.calculate_hop_count(shortest_path)} hops")
    print(f"Total Affected Zones          : {len(affected_zones)}")
    print(f"Repair Crews Dispatched       : {len(repair_crews)}")
    print(f"Fastest Pathfinding Algorithm : BFS")
    print(f"Brute Force Performance       : Slower due to exhaustive traversal")
    
    avg_waiting = scheduler.calculate_average_waiting_time(repair_crews)
    avg_turnaround = scheduler.calculate_average_turnaround_time(repair_crews)
    
    print(f"Average Crew Waiting Time     : {avg_waiting:.2f} hrs")
    print(f"Average Turnaround Time       : {avg_turnaround:.2f} hrs")
    print()
    
    print("=" * 70)
    print(" " * 22 + "Simulation Complete")
    print("=" * 70)


if __name__ == "__main__":
    main()