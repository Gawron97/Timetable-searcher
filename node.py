from datetime import datetime, timedelta
from typing import List


class Node:
    def __init__(self, stop_name, x, y) -> None:
        self.stop_name = stop_name
        self.x = x
        self.y = y
        self.edges: List[Edge] = []
        self.current_cost = 0
        self.estimated_cost = 0
        self.f = 0
        self.changes = 0

    def add_edge(self, line, start_stop, end_stop, departure_time, arrival_time):
        self.edges.append(Edge(line, start_stop, end_stop, departure_time, arrival_time))

    def __lt__(self, other):
        return self.f < other.f

    def __le__(self, other):
        return self.f <= other.f

    def __eq__(self, other):
        return self.stop_name == other.stop_name

    def __ne__(self, other):
        return self.stop_name != other.stop_name

    def __gt__(self, other):
        return self.f > other.f

    def __ge__(self, other):
        return self.f >= other.f
    
    def __str__(self) -> str:
        edges_str = '\n'.join(str(edge) for edge in self.edges)
        return f'stop_name: {self.stop_name}\n edges: {edges_str}'
    
class Edge:
    def __init__(self, line, start_stop: Node, end_stop: Node, departure_time: datetime.time, arrival_time: datetime.time) -> None:
        self.line = line
        self.start_stop = start_stop
        self.end_stop = end_stop
        self.current_cost = 0
        self.estimated_cost = 0
        self.f = 0
        self.departure_time: datetime.time = departure_time
        self.arrival_time: datetime.time = arrival_time

    def __str__(self) -> str:
        return f'{self.line} : {self.start_stop.stop_name} - {self.end_stop.stop_name} | {self.departure_time} :: {self.arrival_time}'
    

    def __lt__(self, other):
        return self.arrival_time <= other.arrival_time
    


class NodeState:
    def __init__(self, line, current_cost, node: Node, edge: Edge, line_changes) -> None:
        self.line = line
        self.current_cost = current_cost
        self.node = node
        self.edge = edge
        self.estimated_cost = 0
        self.f = 0
        self.parent: NodeState = None
        self.line_changes = line_changes

    def __eq__(self, other) -> bool:
        return self.line == other.line and self.node.stop_name == other.node.stop_name
    
    def __str__(self) -> str:
        return f'{self.line} - {self.node.stop_name} - {self.arrival_time}'

    def __lt__(self, other):
        return self.edge.arrival_time < other.edge.arrival_time


