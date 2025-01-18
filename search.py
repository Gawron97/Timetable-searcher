

import random
from node import Node
from algorithms import *


def calculate_cost(nodes_dict: dict[str, Node], route, min_time, criteria_parameter):

    total_time_cost = 0
    total_transfer_cost = 0

    last_line = None
    arrival_time = min_time

    total_path = []

    for i in range(len(route) - 1):
        start_stop, end_stop = route[i], route[i + 1]
        
        if(criteria_parameter == 't'):
            (path, _, time_cost) = dijkstra_time_heura(nodes_dict, start_stop, end_stop, arrival_time)
            arrival_time = path[-1].arrival_time
            total_path += path
            total_time_cost += time_cost
        else:
            (path, _, transfer_cost) = dijkstra_line_heura(nodes_dict, start_stop, end_stop, arrival_time, last_line if(last_line) else None)
            total_transfer_cost += transfer_cost
            last_line = path[-1].line
            arrival_time = path[-1].arrival_time
            total_path += path
                    
    return total_time_cost if criteria_parameter == 't' else total_transfer_cost, total_path


def generate_neighbours(route: list, size):
    neighbours = []

    for _ in range(size):
        new_neighbour = route[:]
        i, j = random.sample(range(1, len(route) - 1), 2)
        new_neighbour[i], new_neighbour[j] = new_neighbour[j], new_neighbour[i]
        neighbours.append(new_neighbour)

    return neighbours


def tabu_search(nodes_dict: dict[str, Node], route, start_time, criteria, iterations, neighbours_size, tabu_size):
    start_execution_time = time.time()
    best_route = route
    best_cost, best_path = calculate_cost(nodes_dict, route, start_time, criteria)
    tabu = []
    

    for _ in range(iterations):
        neighbours = generate_neighbours(best_route, neighbours_size)
        neighbours_cost = []

        neighbours = list(filter(lambda neighbour: neighbour not in tabu, neighbours))
        # neighbours = [neighbour for neighbour in neighbours if neighbour not in tabu]

        if(len(neighbours) == 0):
            continue

        for neighbour in neighbours:
            cost, total_path = calculate_cost(nodes_dict, neighbour, start_time, criteria)
            heapq.heappush(neighbours_cost, (cost, neighbour, total_path))

        (best_neighbour_cost, best_neighbour, total_path) = heapq.heappop(neighbours_cost)

        if(best_neighbour_cost < best_cost):
            best_cost = best_neighbour_cost
            best_route = best_neighbour
            best_path = total_path

            tabu.append(best_neighbour)
            if(len(tabu) > tabu_size):
                tabu.pop(0)

    print('found solution')
    print(f'{best_route} --- {best_cost}')
    return best_cost, best_path, time.time() - start_execution_time
        
