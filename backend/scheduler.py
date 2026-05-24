from collections import deque
from dataclasses import dataclass


@dataclass
class RepairCrew:

    crew_id: str
    burst_time: int
    priority: int
    assigned_station: str

    remaining_time: int
    waiting_time: int = 0
    turnaround_time: int = 0


def create_repair_crew(
    crew_id,
    burst_time,
    assigned_station,
    priority=2
):

    if burst_time <= 0:
        raise ValueError("Burst time must be greater than zero.")

    return RepairCrew(
        crew_id=crew_id,
        burst_time=burst_time,
        remaining_time=burst_time,
        priority=priority,
        assigned_station=assigned_station
    )


def priority_round_robin_schedule(repair_crews, time_quantum):

    if time_quantum <= 0:
        raise ValueError("Time quantum must be greater than zero.")

    current_time = 0
    gantt_chart = []

    # Separate queues by priority
    high_priority = deque(
        [crew for crew in repair_crews if crew.priority == 1]
    )

    medium_priority = deque(
        [crew for crew in repair_crews if crew.priority == 2]
    )

    low_priority = deque(
        [crew for crew in repair_crews if crew.priority == 3]
    )

    while high_priority or medium_priority or low_priority:

       
        if high_priority:
            queue = high_priority

        elif medium_priority:
            queue = medium_priority

        else:
            queue = low_priority

        crew = queue.popleft()

        start_time = current_time

        execution_time = min(
            time_quantum,
            crew.remaining_time
        )

        crew.remaining_time -= execution_time

        current_time += execution_time

        gantt_chart.append(
            (
                crew.crew_id,
                crew.assigned_station,
                start_time,
                current_time,
                crew.priority
            )
        )
        if crew.remaining_time > 0:
            queue.append(crew)

        else:
            crew.turnaround_time = current_time
            crew.waiting_time = (
                crew.turnaround_time - crew.burst_time
            )

    return gantt_chart


def calculate_average_waiting_time(repair_crews):

    total_waiting = sum(
        crew.waiting_time for crew in repair_crews
    )

    return total_waiting / len(repair_crews)


def calculate_average_turnaround_time(repair_crews):

    total_turnaround = sum(
        crew.turnaround_time for crew in repair_crews
    )

    return total_turnaround / len(repair_crews)


def display_gantt_chart(gantt_chart):

    print("Gantt Chart:")
    print("=" * 80)

    for (
        crew_id,
        station,
        start,
        end,
        priority
    ) in gantt_chart:

        print(
            f"[{start:02d}-{end:02d}] "
            f"{crew_id} "
            f"-> {station} "
            f"(Priority {priority})"
        )

    print()


def display_schedule_summary(
    repair_crews,
    time_quantum,
    gantt_chart
):

    print("PacketPath Priority Repair Scheduler")
    print("=" * 50)

    print(f"Time Quantum: {time_quantum}")
    print()

    display_gantt_chart(gantt_chart)

    print("Repair Crew Metrics")
    print("-" * 90)

    print(
        f"{'Crew ID':<10}"
        f"{'Station':<35}"
        f"{'Priority':<10}"
        f"{'Burst':<10}"
        f"{'Waiting':<10}"
        f"{'Turnaround':<12}"
    )

    print("-" * 90)

    for crew in repair_crews:

        print(
            f"{crew.crew_id:<10}"
            f"{crew.assigned_station:<35}"
            f"{crew.priority:<10}"
            f"{crew.burst_time:<10}"
            f"{crew.waiting_time:<10}"
            f"{crew.turnaround_time:<12}"
        )

    print("-" * 90)

    print(
        f"Average Waiting Time: "
        f"{calculate_average_waiting_time(repair_crews):.2f}"
    )

    print(
        f"Average Turnaround Time: "
        f"{calculate_average_turnaround_time(repair_crews):.2f}"
    )


def main():

    time_quantum = 3

    repair_crews = [
        create_repair_crew(
            "Crew-H",
            7,
            "Hospital Emergency Substation",
            priority=1
        ),

        create_repair_crew(
            "Crew-P",
            6,
            "Police Control Substation",
            priority=1
        ),

        create_repair_crew(
            "Crew-A",
            8,
            "Industrial Park Substation",
            priority=2
        ),

        create_repair_crew(
            "Crew-B",
            5,
            "North Grid Substation",
            priority=2
        ),

        create_repair_crew(
            "Crew-C",
            10,
            "Metro Core Substation",
            priority=3
        ),

        create_repair_crew(
            "Crew-D",
            6,
            "Harbor Substation",
            priority=3
        ),
    ]

    gantt_chart = priority_round_robin_schedule(
        repair_crews,
        time_quantum
    )

    display_schedule_summary(
        repair_crews,
        time_quantum,
        gantt_chart
    )


if __name__ == "__main__":
    main()