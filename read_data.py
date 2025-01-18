import csv
from node import *

def normalize_date(date: str):
    date_splitted = date.split(':')
    if(int(date_splitted[0]) <= 23):
        return datetime.strptime(date, '%H:%M:%S')
    else:
        time_delta = timedelta(hours=int(date_splitted[0]), minutes=int(date_splitted[1]), seconds=int(date_splitted[2]))
        time = datetime.strptime('00:00:00', "%H:%M:%S") + time_delta - timedelta(days=1)
        return time

def read_data_to_graf_dict(file_path):
    nodes_dict: dict[str, Node] = {}

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            start_stop_name = (row['start_stop']).lower()
            end_stop_name = (row['end_stop']).lower()
            start_stop_x = float(row['start_stop_lat'])
            start_stop_y = float(row['start_stop_lon'])
            end_stop_x = float(row['end_stop_lat'])
            end_stop_y = float(row['end_stop_lat'])

            if start_stop_name not in nodes_dict:
                nodes_dict[start_stop_name] = Node(start_stop_name, start_stop_x, start_stop_y)
            
            if end_stop_name not in nodes_dict:
                nodes_dict[end_stop_name] = Node(end_stop_name, end_stop_x, end_stop_y)

            line = row['line']
            departure_time = normalize_date(row['departure_time'])
            arrival_time = normalize_date(row['arrival_time'])
            nodes_dict[start_stop_name].add_edge(line, nodes_dict[start_stop_name], nodes_dict[end_stop_name], departure_time, arrival_time)

    for node_name, node in nodes_dict.items():
        node.edges.sort(key=lambda x: x.arrival_time)
    
    return nodes_dict

# file_path = 'connection_graph.csv'
# read_data_to_graf_dict(file_path)
