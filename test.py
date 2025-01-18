import heapq
from functions import *
from node import Edge, Node
from datetime import datetime
import time


def a_star_line_optimized(nodes_dict: dict[str, Node], start, end, min_date: datetime):
    start_time = time.time()

    start_node_state = NodeState("X", 0, min_date, nodes_dict[start])


    opened = [start_node_state]
    closed: list[NodeState] = []

    while opened:

        current_node_state = min(opened, key=lambda x: x.f)

        if(current_node_state.node.stop_name == end):
            break

        opened.remove(current_node_state)
        closed.append(current_node_state)

        for edge in current_node_state.node.edges:
            if((edge.departure_time >= current_node_state.arrival_time
                    or (edge.departure_time.hour == 0 and current_node_state.arrival_time.hour == 23))):
                
                changing_lines = 0
                if(current_node_state.line != edge.line):
                    changing_lines = 1
                
                new_cost = calculate_cost_line_time(current_node_state.current_cost, current_node_state.arrival_time, 
                                                    edge.arrival_time, changing_lines)
                
                next_node_state = NodeState(edge.line, new_cost, edge.arrival_time, edge.end_stop)
                # estimate
                next_node_state.f = next_node_state.current_cost + next_node_state.estimated_cost

                