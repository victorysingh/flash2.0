# PacketPath: Power Grid Routing & Repair Simulation

A comprehensive command-line simulation that models a power grid network, detects faults, and optimizes repair crew dispatch using classic graph traversal and process scheduling algorithms.

---

## 1. Problem Statement

In the event of a power grid failure, utility companies face two critical challenges:
1.  **Rapid Assessment**: Quickly determine the shortest, most efficient route to the fault location for an initial assessment.
2.  **Damage Containment**: Identify the full scope of the outage by mapping all substations and downstream infrastructure affected by the initial fault.
3.  **Resource Management**: Efficiently schedule and manage multiple repair crews to minimize downtime and restore power equitably.

PacketPath simulates this entire workflow, providing a robust solution that leverages fundamental computer science principles to address a real-world logistics and resource management problem.

## 2. Features

-   **Power Grid Modeling**: Represents a complex network of substations and power lines using a graph data structure.
-   **Shortest Path Analysis**: Utilizes Breadth-First Search (BFS) to instantly find the optimal route from a repair depot to a fault location.
-   **Affected Zone Mapping**: Employs Depth-First Search (DFS) to map the entire outage area originating from the fault.
-   **Repair Crew Scheduling**: Simulates repair crews as OS-like processes and schedules them using a Round Robin algorithm to ensure fair and efficient work distribution.
-   **Performance Analytics**: Calculates key OS metrics like **waiting time** and **turnaround time** for each repair crew, along with averages.
-   **Professional CLI**: Presents all findings in a clean, formatted, and easy-to-read command-line interface, perfect for a project demo.

## 3. DAA Concepts Used

-   **Data Structures**:
    -   **Graph (Adjacency List)**: To model the interconnected power grid substations.
    -   **Queue (`collections.deque`)**: For level-order traversal in BFS and for managing the process queue in the Round Robin scheduler.
    -   **Set**: For efficient tracking of visited nodes in graph traversals.
    -   **Dataclass**: To create a clean, structured representation of a repair crew "process".

-   **Algorithms**:
    -   **Breadth-First Search (BFS)**: An unweighted shortest path algorithm.
    -   **Depth-First Search (DFS)**: A graph traversal algorithm for exhaustive exploration.

## 4. OS Concepts Used

-   **Process Simulation**: Repair crews are abstracted as processes, each with a `burst_time` representing the total work required.
-   **CPU Scheduling**: The **Round Robin** scheduling algorithm is implemented to manage how crews are allocated "work time" on the repair task.
-   **Time Quantum**: A configurable time slice is used to ensure that no single crew monopolizes the repair effort, preventing starvation.
-   **Process State Metrics**: The simulation calculates and reports:
    -   **Waiting Time**: The total time a crew spends in the ready queue waiting for its turn.
    -   **Turnaround Time**: The total time from a crew's arrival to its completion.

## 5. Algorithms Implemented

### Breadth-First Search (BFS)
-   **Purpose**: To find the shortest path (in terms of hops) from the `Backup Control Substation` to the `Solar Farm Substation`.
-   **Implementation**: A queue is used to explore the graph layer by layer. This guarantees that when the target node is found, the path taken is the shortest possible in an unweighted graph.

### Depth-First Search (DFS)
-   **Purpose**: To identify every substation affected by the fault at the `Solar Farm Substation`.
-   **Implementation**: A recursive approach is used to explore as far as possible along each branch before backtracking. This ensures all reachable nodes from the fault point are visited and mapped as part of the affected zone.

### Round Robin Scheduling
-   **Purpose**: To fairly schedule the work of four repair crews with varying repair workloads (`burst_time`).
-   **Implementation**: A `deque` acts as a process queue. Each crew is taken from the front, allocated a time slice (quantum), and if its work is not finished, it is sent to the back of the queue. This cycle repeats until all work is done.

## 6. Project Structure

```
PacketPath/
├── graph.py        # Models the power grid using an adjacency list graph.
├── bfs.py          # Implements BFS for shortest path analysis.
├── dfs.py          # Implements DFS for affected zone mapping.
├── scheduler.py    # Implements Round Robin scheduling for repair crews.
└── main.py         # Integrates all modules and runs the final simulation.
```

## 7. How To Run

1.  Ensure you have Python 3.7+ installed.
2.  Place all the Python files (`main.py`, `graph.py`, `bfs.py`, `dfs.py`, `scheduler.py`) in the same directory.
3.  Run the main application from your terminal:

```bash
python main.py
```

## 8. Sample Output

```
======================================================================
          PacketPath: Power Grid Routing & Repair Simulation
======================================================================

[ 1. Loading Power Grid Topology ]
----------------------------------------------------------------------
North Grid Substation -> Central Relay Substation, Hilltop Substation, Wind Ridge Substation
... (graph display) ...

[ 2. Fault Detection Simulation ]
----------------------------------------------------------------------
[!] ALERT: Fault detected at 'Solar Farm Substation'!
[*] Dispatching emergency assessment from 'Backup Control Substation'.

[ 3. BFS: Shortest Path Analysis ]
----------------------------------------------------------------------
PacketPath BFS Route Finder
===============================
Repair Depot: Backup Control Substation
Fault Location: Solar Farm Substation

Traversal Order:
Backup Control Substation -> Central Relay Substation -> Metro Core Substation -> ...

Shortest Path:
Backup Control Substation -> Central Relay Substation -> North Grid Substation -> Wind Ridge Substation -> Greenfield Substation -> Solar Farm Substation
Hop Count: 5

[ 4. DFS: Affected Zone Mapping ]
----------------------------------------------------------------------
PacketPath DFS Affected Zone Mapper
====================================
Fault Node: Solar Farm Substation

Affected Zones:
1. Solar Farm Substation
2. Greenfield Substation
3. Wind Ridge Substation
4. North Grid Substation
...
Total Affected Substations: 18

DFS Traversal Order:
Solar Farm Substation -> Greenfield Substation -> Wind Ridge Substation -> ...

[ 5. Round Robin: Repair Crew Scheduling ]
----------------------------------------------------------------------
PacketPath Round Robin Repair Crew Scheduler
=============================================
Time Quantum: 4

Gantt Chart:
------------------------------------------------------------
| Crew-Alpha (0-4) | Crew-Beta (4-8) | Crew-Gamma (8-12) | Crew-Delta (12-16) | ... |
0                 4                 8                  12                   16   ...

Repair Crew Metrics:
------------------------------------------------------------
Crew ID     Burst     Waiting     Turnaround
------------------------------------------------------------
Crew-Alpha  12        21          33
Crew-Beta   8         21          29
Crew-Gamma  15        26          41
Crew-Delta  6         18          24
------------------------------------------------------------
Average Waiting Time: 21.50
Average Turnaround Time: 31.75

[ 6. Final Simulation Summary ]
----------------------------------------------------------------------
Network Size              : 20 Substations
Fault Location            : Solar Farm Substation
Distance to Fault         : 5 hops
Total Affected Zones      : 18
Repair Crews Dispatched   : 4
Average Crew Waiting Time : 21.50 hrs
Average Turnaround Time   : 31.75 hrs

======================================================================
                      Simulation Complete
======================================================================
```

## 9. Complexity Analysis

-   **BFS (Shortest Path)**: `O(V + E)`
    -   Time: Each vertex (substation) and edge (power line) is visited exactly once.
    -   Space: `O(V)` to store the queue, visited set, and parent map.
-   **DFS (Affected Zone Mapping)**: `O(V + E)`
    -   Time: Each vertex and edge in the connected component is visited once.
    -   Space: `O(V)` for the visited set and recursion stack.
-   **Round Robin Scheduler**: `O(N)` where N is the sum of all burst times.
    -   The total number of operations is proportional to the total work that needs to be done, processed in chunks of `time_quantum`.

## 10. Future Improvements

-   **Dynamic Inputs**: Implement `argparse` to allow the user to specify the start, fault, and time quantum from the command line.
-   **Weighted Graphs**: Enhance the graph with edge weights (e.g., travel time, distance) and implement Dijkstra's algorithm for true real-world shortest path analysis.
-   **Advanced Scheduling**: Implement Priority Scheduling to dispatch more critical crews first.
-   **GUI**: Develop a graphical user interface using a library like Tkinter or PyQT to visualize the graph and scheduling process dynamically.

## 11. Team Contribution

| Member Name      | Contribution                               |
| ---------------- | ------------------------------------------ |
| Jaipreet Singh   | Project Lead, All Modules, Documentation   |
| *(Add Member)*   | *(Add Contribution)*                       |
| *(Add Member)*   | *(Add Contribution)*                       |