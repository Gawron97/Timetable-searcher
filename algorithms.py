import heapq
from functions import *
from node import Edge, Node
from datetime import datetime
import time


def a_star_time_optimized(nodes_dict: dict[str, Node], start, end, min_date: datetime):
    start_time = time.time()

    for node_name, node in nodes_dict.items():
        node.current_cost = 999999999
        node.f = 99999999

    nodes_dict[start].current_cost = 0
    nodes_dict[start].f = 0

    previous_edge: dict[str, Edge] = {node_name: None for node_name, node in nodes_dict.items()}
    previous_edge[start] = Edge("X", Node("Początek", 12, 12), nodes_dict[start], None, arrival_time=min_date)

    opened = [nodes_dict[start]]
    closed = []

    while opened:
        current_node = min(opened, key=lambda x: x.current_cost)

        if(current_node.stop_name == end):
            break
        
        opened.remove(current_node)
        closed.append(current_node)

        if(current_node.stop_name == start):
            min_date_condition = False
        else:
            min_date_condition = True

        for edge in current_node.edges:
            if((min_date_condition or edge.departure_time >= min_date)
               and (edge.departure_time >= previous_edge[current_node.stop_name].arrival_time
                    or (edge.departure_time.hour == 0 and previous_edge[current_node.stop_name].arrival_time.hour == 23))):
            
                next_node: Node = edge.end_stop
                new_cost = calculate_cost_time(current_node.current_cost, previous_edge[current_node.stop_name].arrival_time, edge.arrival_time)
                if(next_node not in opened and next_node not in closed):
                    next_node.current_cost = new_cost
                    opened.append(next_node)
                    previous_edge[next_node.stop_name] = edge
                elif(next_node.current_cost > new_cost):
                    next_node.current_cost = new_cost
                    previous_edge[next_node.stop_name] = edge
                    if(next_node in closed):
                        opened.append(next_node)
                        closed.remove(next_node)
    
    return previous_edge, (time.time() - start_time), (previous_edge[end].arrival_time - min_date).total_seconds() / 60



def a_star_time_optimized_heura(nodes_dict: dict[str, Node], start, end, min_date: datetime):
    start_time = time.time()

    for node_name, node in nodes_dict.items():
        node.current_cost = 999999999
        node.f = 99999999

    nodes_dict[start].current_cost = 0
    nodes_dict[start].f = 0

    previous_edge: dict[str, Edge] = {node_name: None for node_name, node in nodes_dict.items()}
    previous_edge[start] = Edge("X", Node("Początek", 12, 12), nodes_dict[start], None, arrival_time=min_date)

    opened = [nodes_dict[start]]
    closed = []

    while opened:
        current_node = min(opened, key=lambda x: x.f)

        if(current_node.stop_name == end):
            break
        
        opened.remove(current_node)
        closed.append(current_node)

        for edge in current_node.edges:
            if((edge.departure_time >= previous_edge[current_node.stop_name].arrival_time
                    or (edge.departure_time.hour == 0 and previous_edge[current_node.stop_name].arrival_time.hour == 23))):
            
                next_node: Node = edge.end_stop
                new_cost = calculate_cost_time(current_node.current_cost, previous_edge[current_node.stop_name].arrival_time, edge.arrival_time)
                if(next_node not in opened and next_node not in closed):
                    next_node.current_cost = new_cost
                    next_node.estimated_cost = estimate_cost_time(next_node, nodes_dict[end])
                    next_node.f = next_node.current_cost + next_node.estimated_cost
                    opened.append(next_node)
                    previous_edge[next_node.stop_name] = edge
                elif(next_node.current_cost > new_cost):
                    next_node.current_cost = new_cost
                    next_node.f = next_node.current_cost + next_node.estimated_cost
                    previous_edge[next_node.stop_name] = edge
                    if(next_node in closed):
                        opened.append(next_node)
                        closed.remove(next_node)
    
    return previous_edge, (time.time() - start_time), (previous_edge[end].arrival_time - min_date).total_seconds() / 60



def a_star_line_optimized(nodes_dict: dict[str, Node], start, end, min_date: datetime, start_line = 'X'):
    start_time = time.time()

    start_edge = Edge(start_line, Node("Początek", 12, 12), nodes_dict[start], None, arrival_time=min_date)
    start_node_state = NodeState(start_line, 0, nodes_dict[start], start_edge, 0)

    opened = [start_node_state]
    closed: list[NodeState] = []

    found_node_state = None

    while opened:

        current_node_state = min(opened, key=lambda x: x.current_cost)

        if(current_node_state.node.stop_name == end):
            found_node_state = current_node_state
            break

        opened.remove(current_node_state)
        closed.append(current_node_state)

        for edge in current_node_state.node.edges:
            if((edge.departure_time >= current_node_state.edge.arrival_time
                    or (edge.departure_time.hour == 0 and current_node_state.edge.arrival_time.hour == 23))):
                
                changing_lines = 0
                if(current_node_state.line != edge.line):
                    changing_lines = 1
                
                new_cost = calculate_cost_line_time(current_node_state.current_cost, current_node_state.edge.arrival_time, 
                                                    edge.arrival_time, changing_lines)
                
                next_node_state = NodeState(edge.line, new_cost, edge.end_stop, edge, current_node_state.line_changes + changing_lines)

                if(opened.count(next_node_state) > 0):
                    node_in_open = opened[opened.index(next_node_state)]
                    if(node_in_open.current_cost > new_cost):
                        node_in_open.current_cost = new_cost
                        node_in_open.line_changes = current_node_state.line_changes + changing_lines
                        node_in_open.parent = current_node_state
                        node_in_open.edge = edge
                
                elif(closed.count(next_node_state) > 0):
                    node_in_closed = closed[closed.index(next_node_state)]
                    if(node_in_closed.current_cost > new_cost):
                        node_in_closed.current_cost = new_cost
                        node_in_closed.line_changes = current_node_state.line_changes + changing_lines
                        node_in_closed.parent = current_node_state
                        node_in_closed.edge = edge
                        opened.append(node_in_closed)
                        closed.remove(node_in_closed)

                else:
                    next_node_state.current_cost = new_cost
                    next_node_state.parent = current_node_state
                    next_node_state.edge = edge
                    opened.append(next_node_state)

    return (found_node_state, time.time() - start_time, found_node_state.line_changes)


def a_star_line_optimized_heura(nodes_dict: dict[str, Node], start, end, min_date: datetime, start_line = 'X'):
    start_time = time.time()

    start_edge = Edge(start_line, Node("Początek", 12, 12), nodes_dict[start], None, arrival_time=min_date)
    start_node_state = NodeState(start_line, 0, nodes_dict[start], start_edge, 0)

    opened = [start_node_state]
    closed: list[NodeState] = []

    found_node_state = None

    while opened:

        current_node_state = min(opened, key=lambda x: x.f)

        if(current_node_state.node.stop_name == end):
            found_node_state = current_node_state
            break

        opened.remove(current_node_state)
        closed.append(current_node_state)

        for edge in current_node_state.node.edges:
            if((edge.departure_time >= current_node_state.edge.arrival_time
                    or (edge.departure_time.hour == 0 and current_node_state.edge.arrival_time.hour == 23))):
                
                changing_lines = 0
                if(current_node_state.line != edge.line):
                    changing_lines = 1
                
                new_cost = calculate_cost_line_time(current_node_state.current_cost, current_node_state.edge.arrival_time, 
                                                    edge.arrival_time, changing_lines)
                
                next_node_state = NodeState(edge.line, new_cost, edge.end_stop, edge, current_node_state.line_changes + changing_lines)

                if(opened.count(next_node_state) > 0):
                    node_in_open = opened[opened.index(next_node_state)]
                    if(node_in_open.current_cost > new_cost):
                        node_in_open.current_cost = new_cost
                        node_in_open.f = node_in_open.current_cost + node_in_open.estimated_cost
                        node_in_open.line_changes = current_node_state.line_changes + changing_lines
                        node_in_open.parent = current_node_state
                        node_in_open.edge = edge
                
                elif(closed.count(next_node_state) > 0):
                    node_in_closed = closed[closed.index(next_node_state)]
                    if(node_in_closed.current_cost > new_cost):
                        node_in_closed.current_cost = new_cost
                        node_in_closed.f = node_in_closed.current_cost + node_in_closed.estimated_cost
                        node_in_closed.line_changes = current_node_state.line_changes + changing_lines
                        node_in_closed.parent = current_node_state
                        node_in_closed.edge = edge
                        opened.append(node_in_closed)
                        closed.remove(node_in_closed)
                else:
                    estimated_cost = estimate_cost_time(current_node_state.node, nodes_dict[end])
                    next_node_state.current_cost = new_cost
                    next_node_state.estimated_cost = estimated_cost
                    next_node_state.f = next_node_state.current_cost + next_node_state.estimated_cost
                    next_node_state.parent = current_node_state
                    next_node_state.edge = edge
                    opened.append(next_node_state)

    return (found_node_state, time.time() - start_time, found_node_state.line_changes)




def dijkstra_time(nodes_dict: dict[str, Node], start, end, min_date: datetime):
    start_time = time.time()

    for node_name, node in nodes_dict.items():
        node.current_cost = 99999999
    
    nodes_dict[start].current_cost = 0

    path = [Edge("X", Node("Początek", 12, 12), nodes_dict[start], None, arrival_time=min_date)]

    priority_queue = [(0, min_date, nodes_dict[start], path)]

    while priority_queue:
        (current_cost, current_arrival_time, current_node, current_path) = heapq.heappop(priority_queue)

        if(current_node == nodes_dict[end]):
            path = current_path
            break

        for edge in current_node.edges:
            if(edge.departure_time >= current_arrival_time or (edge.departure_time.hour == 0 and current_arrival_time.hour == 23)):

                next_node: Node = edge.end_stop
                new_cost = calculate_cost_time(current_cost, current_arrival_time, edge.arrival_time)
                if(new_cost < next_node.current_cost):
                    next_node.current_cost = new_cost

                    new_path = current_path.copy()
                    new_path.append(edge)

                    heapq.heappush(priority_queue, (new_cost, edge.arrival_time, next_node, new_path))

    return path, (time.time() - start_time), (path[-1].arrival_time - min_date).total_seconds() / 60

def dijkstra_time_heura(nodes_dict: dict[str, Node], start, end, min_date: datetime):
    start_time = time.time()

    for node_name, node in nodes_dict.items():
        node.current_cost = 99999999
        node.f = 99999999

    nodes_dict[start].current_cost = 0
    nodes_dict[start].f = 0
    
    path = [Edge("X", Node("Początek", 12, 12), nodes_dict[start], None, arrival_time=min_date)]

    priority_queue = [(0, 0, min_date, nodes_dict[start], path)]

    while priority_queue:
        (current_f, current_cost, current_arrival_time, current_node, current_path) = heapq.heappop(priority_queue)

        if(current_node == nodes_dict[end]):
            path = current_path
            break

        for edge in current_node.edges:
            if(edge.departure_time >= current_arrival_time or (edge.departure_time.hour == 0 and current_arrival_time.hour == 23)):

                next_node: Node = edge.end_stop
                new_cost = calculate_cost_time(current_cost, current_arrival_time, edge.arrival_time)
                estimated_cost = estimate_cost_time(next_node, nodes_dict[end])
                if(next_node.current_cost > new_cost):
                    
                    next_node.current_cost = new_cost
                    next_node.estimated_cost = estimated_cost
                    next_node.f = next_node.current_cost + next_node.estimated_cost

                    new_path = current_path.copy()
                    new_path.append(edge)

                    heapq.heappush(priority_queue, (next_node.f, next_node.current_cost, edge.arrival_time, next_node, new_path))

    return path, (time.time() - start_time), (path[-1].arrival_time - min_date).total_seconds() / 60


def dijkstra_line(nodes_dict: dict[str, Node], start, end, min_date: datetime, start_line = None):
    start_time = time.time()
    
    nodes_dict[start].current_cost = 0

    transfers = {}
    start_line_to_set = None
    if(start_line is None):
        start_line_to_set = 'X'
    path = [Edge(start_line_to_set, Node("Początek", 12, 12), nodes_dict[start], None, arrival_time=min_date)]

    priority_queue = [(0, 0, start_line_to_set, min_date, nodes_dict[start], path)]
    lines_to_change = 0

    while priority_queue:
        print(len(priority_queue))
        (current_cost, line_changes, current_line, current_arrival_time, current_node, current_path) = heapq.heappop(priority_queue)
        
        if(current_node == nodes_dict[end]):
            lines_to_change = (line_changes - 1) if start_line is None else line_changes
            path = current_path
            break


        for edge in current_node.edges:
            if(edge.departure_time >= current_arrival_time or (edge.departure_time.hour == 0 and current_arrival_time.hour == 23)):

                changing_lines = 1 if current_line != edge.line else 0
                new_lines_changes = line_changes + changing_lines

                next_stop: Node = edge.end_stop
                transfer_key = f'{edge.line}_{current_node.stop_name}_{next_stop.stop_name}'
                if(transfer_key not in transfers or new_lines_changes < transfers[transfer_key]):
                    transfers[transfer_key] = new_lines_changes
                    next_cost = calculate_cost_line_time(current_cost, current_arrival_time, edge.arrival_time, changing_lines)

                    new_path = current_path.copy()
                    new_path.append(edge)
            
                    heapq.heappush(priority_queue, (next_cost, new_lines_changes, edge.line, edge.arrival_time, next_stop, new_path))

    return path, (time.time() - start_time), lines_to_change



def dijkstra_line_heura(nodes_dict: dict[str, Node], start, end, min_date: datetime, start_line = None):
    start_time = time.time()
    
    nodes_dict[start].current_cost = 0
    nodes_dict[start].f = 0

    transfers = {}
    start_line_to_set = None
    if(start_line is None):
        start_line_to_set = 'X'

    path = [Edge(start_line_to_set, Node("Początek", 12, 12), nodes_dict[start], None, arrival_time=min_date)]

    priority_queue = [(0, 0, 0, start_line_to_set, min_date, nodes_dict[start], path)]
    lines_to_change = 0

    while priority_queue:
        (current_f, current_cost, line_changes, current_line, current_arrival_time, current_node, current_path) = heapq.heappop(priority_queue)
        
        if(current_node == nodes_dict[end]):
            lines_to_change = (line_changes - 1) if start_line is None else line_changes
            path = current_path
            break


        for edge in current_node.edges:
            if(edge.departure_time >= current_arrival_time or (edge.departure_time.hour == 0 and current_arrival_time.hour == 23)):

                changing_lines = 1 if current_line != edge.line else 0
                new_lines_changes = line_changes + changing_lines

                next_stop: Node = edge.end_stop
                transfer_key = f'{edge.line}_{current_node.stop_name}_{next_stop.stop_name}'
                if(transfer_key not in transfers or new_lines_changes < transfers[transfer_key]):
                    transfers[transfer_key] = new_lines_changes
                    next_cost = calculate_cost_line_time(current_cost, current_arrival_time, edge.arrival_time, changing_lines)
                    estimated_cost = estimate_cost_time(next_stop, nodes_dict[end])
                    f = next_cost + estimated_cost

                    new_path = current_path.copy()
                    new_path.append(edge)
            
                    heapq.heappush(priority_queue, (f, next_cost, new_lines_changes, edge.line, edge.arrival_time, next_stop, new_path))


    return path, (time.time() - start_time), lines_to_change