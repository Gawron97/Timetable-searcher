from node import Edge, Node, NodeState
from datetime import datetime, timedelta

def calculate_cost_line_time(current_node_cost, current_stop_arrival_time, next_stop_arrival_time, changing_line):
    return calculate_cost_time(current_node_cost, current_stop_arrival_time, next_stop_arrival_time) + calculate_cost_line(changing_line)

def calculate_cost_line(changing_line):
    return changing_line * 100

def calculate_cost_time(current_node_cost, current_stop_arrival_time, next_stop_arrival_time):
    return current_node_cost + calculate_distance_time(current_stop_arrival_time, next_stop_arrival_time)

def calculate_distance_time(current_stop_arrival_time, next_stop_arrival_time):
    if(next_stop_arrival_time < current_stop_arrival_time):
        midnight = datetime.strptime('00:00:00', "%H:%M:%S")
        duration = next_stop_arrival_time - midnight
        midnight += timedelta(days=1)
        duration += midnight - current_stop_arrival_time
    else:
        duration = next_stop_arrival_time - current_stop_arrival_time
    return duration.total_seconds() / 60.0

def estimate_cost_time(start_node: Node, end_node: Node):
    euclidan_distance = ((start_node.x - end_node.x) ** 2 + (start_node.y - end_node.y) ** 2) ** 0.5
    return euclidan_distance * 400

def get_best_node(nodes: list[Node]):
    best_node = nodes[0]
    for node in nodes:
        if(node.f < best_node.f):
            best_node = node

    return best_node

def get_best_node_exp(nodes: list[NodeState]):
    best_node = nodes[0]
    for node in nodes:
        if(node.f < best_node.f):
            best_node = node

    return best_node

def get_best_path_from_dict(previous_edge, end: Node):
    path = []
    current_edge: Edge = previous_edge[end.stop_name]

    while current_edge is not None:
        path.insert(0, f'line: {current_edge.line} | start_stop: {current_edge.start_stop.stop_name} : {current_edge.departure_time.strftime("%H:%M:%S") if current_edge.departure_time else ""} - end_stop: {current_edge.end_stop.stop_name} : {datetime.strftime(current_edge.arrival_time, "%H:%M:%S")}')
        current_edge: Edge = previous_edge.get(current_edge.start_stop.stop_name, None)

    return path

def get_best_path_from_list(path: list[Edge]):

    styled_path = []

    for current_edge in path:
        styled_path.append(f'line: {current_edge.line} | start_stop: {current_edge.start_stop.stop_name} : {current_edge.departure_time.strftime("%H:%M:%S") if current_edge.departure_time else ""} - end_stop: {current_edge.end_stop.stop_name} : {datetime.strftime(current_edge.arrival_time, "%H:%M:%S")}')

    return styled_path

def get_best_path_with_transfers_only(path: list[Edge]):
    styled_path = []

    prev_edge = path[0]
    styled_path.append(f'line: {prev_edge.line} - start_stop: {prev_edge.start_stop.stop_name}  ::  {prev_edge.departure_time.strftime("%H:%M:%S") if prev_edge.departure_time else ""}')

    for current_edge in path[1:]:
        if(current_edge.line != prev_edge.line):
            styled_path.append(f'line: {prev_edge.line} - end_stop: {prev_edge.end_stop.stop_name} :: {datetime.strftime(prev_edge.arrival_time, "%H:%M:%S")} line: {current_edge.line} - start_stop: {current_edge.start_stop.stop_name} :: {current_edge.departure_time.strftime("%H:%M:%S") if current_edge.departure_time else ""}')

        prev_edge = current_edge
    styled_path.append(f'line: {prev_edge.line} - end_stop: {prev_edge.end_stop.stop_name}  ::  {prev_edge.arrival_time}')

    return styled_path

def get_best_path_from_node(path: NodeState):

    styled_path = []

    current_node_state = path

    while current_node_state:
        styled_path.insert(0, f'line: {current_node_state.line} | start_stop: {current_node_state.edge.start_stop.stop_name} : {current_node_state.edge.departure_time.strftime("%H:%M:%S") if current_node_state.edge.departure_time else ""} - end_stop: {current_node_state.node.stop_name} : {datetime.strftime(current_node_state.edge.arrival_time, "%H:%M:%S")}')
        current_node_state = current_node_state.parent
    
    return styled_path