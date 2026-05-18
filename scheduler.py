"""
PacketPath repair crew scheduler.

This module simulates repair crews as OS-like processes and schedules them
using the Round Robin CPU scheduling algorithm.
"""

from collections import deque
from dataclasses import dataclass


@dataclass
class RepairCrew:
    """Repair crew represented as a schedulable process."""

    crew_id: str
    burst_time: int
    remaining_time: int
    waiting_time: int = 0
    turnaround_time: int = 0


def create_repair_crew(crew_id, burst_time):
    """
    Create a repair crew process.

    Args:
        crew_id (str): Unique repair crew identifier.
        burst_time (int): Total time required by the crew to complete repairs.

    Returns:
        RepairCrew: Initialized repair crew process.
    """
    if burst_time <= 0:
        raise ValueError("Burst time must be greater than zero.")

    return RepairCrew(
        crew_id=crew_id,
        burst_time=burst_time,
        remaining_time=burst_time,
    )


def round_robin_schedule(repair_crews, time_quantum):
    """
    Schedule repair crews using Round Robin scheduling.

    Each crew receives up to time_quantum units in cyclic order until all crews
    complete their assigned repair work.

    Args:
        repair_crews (list[RepairCrew]): Repair crews to schedule.
        time_quantum (int): Maximum time slice assigned per turn.

    Returns:
        list[tuple[str, int, int]]: Gantt chart entries as
        (crew_id, start_time, end_time).
    """
    if time_quantum <= 0:
        raise ValueError("Time quantum must be greater than zero.")

    current_time = 0
    gantt_chart = []
    
    # Utilize a deque for true Round Robin process queueing
    queue = deque(repair_crews)

    while queue:
        crew = queue.popleft()

        start_time = current_time
        execution_time = min(time_quantum, crew.remaining_time)

        crew.remaining_time -= execution_time
        current_time += execution_time
        gantt_chart.append((crew.crew_id, start_time, current_time))

        if crew.remaining_time > 0:
            # Requeue the crew if they still have remaining work
            queue.append(crew)
        else:
            # Since all crews arrive at time 0, completion time is turnaround
            # time. Waiting time is turnaround time minus burst time.
            crew.turnaround_time = current_time
            crew.waiting_time = crew.turnaround_time - crew.burst_time

    return gantt_chart


def calculate_average_waiting_time(repair_crews):
    """Calculate average waiting time for all repair crews."""
    total_waiting_time = sum(crew.waiting_time for crew in repair_crews)
    return total_waiting_time / len(repair_crews)


def calculate_average_turnaround_time(repair_crews):
    """Calculate average turnaround time for all repair crews."""
    total_turnaround_time = sum(crew.turnaround_time for crew in repair_crews)
    return total_turnaround_time / len(repair_crews)


def display_gantt_chart(gantt_chart):
    """
    Display a readable Gantt chart for the Round Robin schedule.

    Args:
        gantt_chart (list[tuple[str, int, int]]): Schedule entries.
    """
    print("Gantt Chart:")
    print("-" * 60)

    timeline = ""
    time_markers = ""

    for crew_id, start_time, end_time in gantt_chart:
        block = f"| {crew_id} ({start_time}-{end_time}) "
        timeline += block
        time_markers += f"{start_time:<{len(block)}}"

    timeline += "|"

    if gantt_chart:
        time_markers += str(gantt_chart[-1][2])

    print(timeline)
    print(time_markers)
    print()


def display_schedule_summary(repair_crews, time_quantum, gantt_chart):
    """
    Display the final scheduling report.

    Args:
        repair_crews (list[RepairCrew]): Scheduled repair crews.
        time_quantum (int): Time quantum used for Round Robin scheduling.
        gantt_chart (list[tuple[str, int, int]]): Generated Gantt chart.
    """
    print("PacketPath Round Robin Repair Crew Scheduler")
    print("=" * 45)
    print(f"Time Quantum: {time_quantum}")
    print()

    display_gantt_chart(gantt_chart)

    print("Repair Crew Metrics:")
    print("-" * 60)
    print(f"{'Crew ID':<12}{'Burst':<10}{'Waiting':<12}{'Turnaround':<12}")
    print("-" * 60)

    for crew in repair_crews:
        print(
            f"{crew.crew_id:<12}"
            f"{crew.burst_time:<10}"
            f"{crew.waiting_time:<12}"
            f"{crew.turnaround_time:<12}"
        )

    print("-" * 60)
    print(f"Average Waiting Time: {calculate_average_waiting_time(repair_crews):.2f}")
    print(
        "Average Turnaround Time: "
        f"{calculate_average_turnaround_time(repair_crews):.2f}"
    )


def main():
    """Run a PacketPath Round Robin scheduling demo."""
    time_quantum = 3
    repair_crews = [
        create_repair_crew("Crew-A", 8),
        create_repair_crew("Crew-B", 5),
        create_repair_crew("Crew-C", 10),
        create_repair_crew("Crew-D", 6),
    ]

    gantt_chart = round_robin_schedule(repair_crews, time_quantum)
    display_schedule_summary(repair_crews, time_quantum, gantt_chart)


if __name__ == "__main__":
    main()