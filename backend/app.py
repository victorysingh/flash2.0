from flask import Flask, jsonify, request
from flask_cors import CORS
import time

from graph import create_packetpath_graph
import bfs
import dfs
import scheduler
import brute_force

app = Flask(__name__)
CORS(app)


# =========================================================
# BFS ROUTE ANALYSIS
# =========================================================
@app.route('/bfs', methods=['GET'])
def run_bfs():

    start = request.args.get(
        'start',
        'Backup Control Substation'
    )

    target = request.args.get(
        'target',
        'Solar Farm Substation'
    )

    graph = create_packetpath_graph()

    try:

        traversal_order, shortest_path = (
            bfs.breadth_first_search(
                graph,
                start,
                target
            )
        )

        hop_count = bfs.calculate_hop_count(
            shortest_path
        )

        return jsonify({

            "status": "success",

            "start": start,

            "target": target,

            "traversal_order": traversal_order,

            "shortest_path": shortest_path,

            "hop_count": hop_count

        })

    except ValueError as e:

        return jsonify({

            "status": "error",
            "message": str(e)

        }), 400



@app.route('/dfs', methods=['GET'])
def run_dfs():

    fault_node = request.args.get(
        'fault_node',
        'Central Relay Substation'
    )

    graph = create_packetpath_graph()

    try:

        affected_zones, traversal_order = (
            dfs.find_affected_substations(
                graph,
                fault_node
            )
        )

        return jsonify({

            "status": "success",

            "fault_node": fault_node,

            "affected_zones": list(
                affected_zones
            ),

            "traversal_order": traversal_order,

            "total_affected": len(
                affected_zones
            )

        })

    except ValueError as e:

        return jsonify({

            "status": "error",
            "message": str(e)

        }), 400


@app.route('/scheduler', methods=['GET'])
def run_scheduler():

    try:

        time_quantum = int(
            request.args.get(
                'time_quantum',
                3
            )
        )

    except ValueError:

        return jsonify({

            "status": "error",

            "message":
            "time_quantum must be integer"

        }), 400

    try:

        repair_crews = [

            # HIGH PRIORITY
            scheduler.create_repair_crew(
                "Crew-H",
                7,
                "Hospital Emergency Substation",
                priority=1
            ),

            scheduler.create_repair_crew(
                "Crew-P",
                6,
                "Police Control Substation",
                priority=1
            ),

            # MEDIUM PRIORITY
            scheduler.create_repair_crew(
                "Crew-A",
                8,
                "Industrial Park Substation",
                priority=2
            ),

            scheduler.create_repair_crew(
                "Crew-B",
                5,
                "North Grid Substation",
                priority=2
            ),

           
            scheduler.create_repair_crew(
                "Crew-C",
                10,
                "Metro Core Substation",
                priority=3
            ),

            scheduler.create_repair_crew(
                "Crew-D",
                6,
                "Harbor Substation",
                priority=3
            )

        ]

        gantt_chart = (
            scheduler.priority_round_robin_schedule(
                repair_crews,
                time_quantum
            )
        )

        avg_wait = (
            scheduler.calculate_average_waiting_time(
                repair_crews
            )
        )

        avg_turnaround = (
            scheduler.calculate_average_turnaround_time(
                repair_crews
            )
        )

        crews_data = []

        for crew in repair_crews:

            crews_data.append({

                "crew_id":
                crew.crew_id,

                "assigned_station":
                crew.assigned_station,

                "priority":
                crew.priority,

                "burst_time":
                crew.burst_time,

                "waiting_time":
                crew.waiting_time,

                "turnaround_time":
                crew.turnaround_time

            })

        gantt_data = []

        for g in gantt_chart:

            gantt_data.append({

                "crew_id": g[0],

                "station": g[1],

                "start_time": g[2],

                "end_time": g[3],

                "priority": g[4]

            })

        return jsonify({

            "status": "success",

            "scheduler_type":
            "Priority Round Robin",

            "time_quantum":
            time_quantum,

            "gantt_chart":
            gantt_data,

            "crews":
            crews_data,

            "average_waiting_time":
            avg_wait,

            "average_turnaround_time":
            avg_turnaround

        })

    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 400

@app.route('/compare', methods=['GET'])
def run_compare():

    start = request.args.get(
        'start',
        'Backup Control Substation'
    )

    target = request.args.get(
        'target',
        'North Grid Substation'
    )

    graph = create_packetpath_graph()

    try:

        bf_path, bf_time = (
            brute_force.find_shortest_path_brute_force(
                graph,
                start,
                target
            )
        )

        bf_hop_count = (
            bfs.calculate_hop_count(bf_path)
            if bf_path else 0
        )

        # =====================================
        # BFS
        # =====================================

        start_time_bfs = time.perf_counter()

        _, bfs_path = bfs.breadth_first_search(
            graph,
            start,
            target
        )

        end_time_bfs = time.perf_counter()

        bfs_time = (
            end_time_bfs - start_time_bfs
        )

        bfs_hop_count = (
            bfs.calculate_hop_count(
                bfs_path
            )
            if bfs_path else 0
        )

        if bfs_time > 0:

            speed_factor = (
                bf_time / bfs_time
            )

        else:

            speed_factor = 0

        return jsonify({

            "status": "success",

            "start": start,

            "target": target,

            "performance_summary": {

                "faster_algorithm":
                "BFS",

                "speed_factor":
                round(speed_factor, 2)

            },

            "brute_force": {

                "algorithm":
                "Recursive Brute Force",

                "path":
                bf_path,

                "hop_count":
                bf_hop_count,

                "time":
                bf_time

            },

            "bfs": {

                "algorithm":
                "Breadth First Search",

                "path":
                bfs_path,

                "hop_count":
                bfs_hop_count,

                "time":
                bfs_time

            }

        })

    except ValueError as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 400

@app.route('/', methods=['GET'])
def home():

    return jsonify({

        "project": "PacketPath",

        "status": "running",

        "apis": [

            "/bfs",
            "/dfs",
            "/scheduler",
            "/compare"

        ]

    })

if __name__ == '__main__':

    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )