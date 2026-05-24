from graph import create_packetpath_graph


def recursive_dfs(
    graph,
    current_node,
    visited,
    traversal_order,
    current_depth,
    max_depth
):
    if current_depth > max_depth:
        return

    visited.add(current_node)

    traversal_order.append(current_node)

    for neighbor in graph.adjacency_list[current_node]:

        if neighbor not in visited:

            recursive_dfs(
                graph,
                neighbor,
                visited,
                traversal_order,
                current_depth + 1,
                max_depth
            )


def find_affected_substations(
    graph,
    fault_node,
    max_depth=2
):

    if fault_node not in graph.adjacency_list:

        raise ValueError(
            f"Fault node not found in graph: {fault_node}"
        )

    visited = set()

    traversal_order = []

    recursive_dfs(
        graph,
        fault_node,
        visited,
        traversal_order,
        current_depth=0,
        max_depth=max_depth
    )

    return visited, traversal_order


def display_dfs_result(
    fault_node,
    affected_zones,
    traversal_order
):

    print("PacketPath DFS Affected Zone Mapper")

    print("=" * 40)

    print(f"Fault Node: {fault_node}")

    print()

    print("Affected Zones:")

    for index, substation in enumerate(
        traversal_order,
        start=1
    ):

        print(f"{index}. {substation}")

    print()

    print(
        f"Total Affected Substations: "
        f"{len(affected_zones)}"
    )

    print()

    print("DFS Traversal Order:")

    print(" -> ".join(traversal_order))


def main():

    packetpath_graph = create_packetpath_graph()

    fault_node = "Central Relay Substation"

    affected_zones, traversal_order = (
        find_affected_substations(
            packetpath_graph,
            fault_node,
            max_depth=2
        )
    )

    display_dfs_result(
        fault_node,
        affected_zones,
        traversal_order
    )


if __name__ == "__main__":

    main()