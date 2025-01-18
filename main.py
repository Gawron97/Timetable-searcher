


from datetime import datetime
from algorithms import *
from read_data import read_data_to_graf_dict
from search import *


file_path = 'connection_graph.csv'
graph = read_data_to_graf_dict(file_path)
# (path, execution_time, cost) = dijkstra_time(graph, 'kminkowa', 'brochów', datetime.strptime('18:00:00', '%H:%M:%S'))
# print(f'execution_time: {execution_time:.2f}')
# print(cost)
# styled_path = get_best_path_from_list(path)
# print('\n'.join(styled_path))

cost, path, execution_time = tabu_search(graph, ['trzebnicka', 'krzyki', 'dworzec nadodrze', 'psie pole', 'dworzec główny', 'komandorska', 'trzebnicka'], datetime.strptime('18:00:00', '%H:%M:%S'), 't', 10, 4, 10)
print(f'execution_time: {execution_time}')
print(f'cost: {cost}')
styled_path = get_best_path_with_transfers_only(path)
print('\n'.join(styled_path))
