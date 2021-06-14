"""Simple travelling salesman problem between cities."""
from __future__ import division
from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

import json
import urllib.request as ur
import datetime

def receive_input():
    addresses = []
    labels = []
    num = 1
    while True:
        address = input('Address {}: '.format(num))
        if address == "done":
            break
        labels.append(address)
        address = address.replace(" ", "+")
        addresses.append(address)
        num += 1
    return addresses, labels

def create_data(addresses):
  """Creates the data."""
  data = {}
  data['API_key'] = 'API KEY'
  data['addresses'] = addresses
  return data

def create_distance_duration_matrix(data):
  addresses = data["addresses"]
  API_key = data["API_key"]
  # Distance Matrix API only accepts 100 elements per request, so get rows in multiple requests.
  max_elements = 100
  num_addresses = len(addresses) # 16 in this example.
  # Maximum number of rows that can be computed per request (6 in this example).
  max_rows = max_elements // num_addresses
  # num_addresses = q * max_rows + r (q = 2 and r = 4 in this example).
  q, r = divmod(num_addresses, max_rows)
  dest_addresses = addresses
  distance_matrix = []
  duration_matrix = []
  # Send q requests, returning max_rows rows per request.
  for i in range(q):
    origin_addresses = addresses[i * max_rows: (i + 1) * max_rows]
    response = send_request(origin_addresses, dest_addresses, API_key)
    distance_matrix += build_distance_matrix(response)
    duration_matrix += build_duration_matrix(response)
    
  # Get the remaining remaining r rows, if necessary.
  if r > 0:
    origin_addresses = addresses[q * max_rows: q * max_rows + r]
    response = send_request(origin_addresses, dest_addresses, API_key)
    distance_matrix += build_distance_matrix(response)
    duration_matrix += build_duration_matrix(response)
  return distance_matrix, duration_matrix

def send_request(origin_addresses, dest_addresses, API_key):
  """ Build and send request for the given origin and destination addresses."""
  def build_address_str(addresses):
    # Build a pipe-separated string of addresses
    address_str = ''
    for i in range(len(addresses) - 1):
      address_str += addresses[i] + '|'
    address_str += addresses[-1]
    return address_str

  request = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial'
  origin_address_str = build_address_str(origin_addresses)
  dest_address_str = build_address_str(dest_addresses)
  request = request + '&origins=' + origin_address_str + '&destinations=' + \
                       dest_address_str + '&key=' + API_key
  jsonResult = ur.urlopen(request).read()
  response = json.loads(jsonResult)
  return response

def build_distance_matrix(response):
  distance_matrix = []
  for row in response['rows']:
    row_list = [row['elements'][j]['distance']['value'] for j in range(len(row['elements']))]
    distance_matrix.append(row_list)
  return distance_matrix

def build_duration_matrix(response):
  duration_matrix = []
  for row in response['rows']:
    row_list = [row['elements'][j]['duration']['value'] for j in range(len(row['elements']))]
    duration_matrix.append(row_list)
  return duration_matrix

def create_data_model(distance_matrix, duration_matrix):
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = distance_matrix
    data['duration_matrix'] = duration_matrix
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data

def print_distance_solution(manager, distance_routing, duration_routing, solution, labels):
    """Prints solution on console."""
    index = distance_routing.Start(0)
    plan_output = '\nRoute based on shortest distance:\n'
    route_distance = 0
    route_duration = 0
    while not distance_routing.IsEnd(index):
        plan_output += ' {} ->'.format(labels[manager.IndexToNode(index)])
        previous_index = index
        index = solution.Value(distance_routing.NextVar(index))
        route_distance += distance_routing.GetArcCostForVehicle(previous_index, index, 0)
        route_duration += duration_routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(labels[manager.IndexToNode(index)])
    plan_output += 'Route distance: {}miles\n'.format(route_distance)
    plan_output += 'Route duration: {}\n'.format(datetime.timedelta(seconds=route_duration))
    print(plan_output)

def print_duration_solution(manager, duration_routing, distance_routing, solution, labels):
    """Prints solution on console."""
    index = duration_routing.Start(0)
    plan_output = 'Route based on shortest duration:\n'
    route_duration = 0
    route_distance = 0
    while not duration_routing.IsEnd(index):
        plan_output += ' {} ->'.format(labels[manager.IndexToNode(index)])
        previous_index = index
        index = solution.Value(duration_routing.NextVar(index))
        route_duration += duration_routing.GetArcCostForVehicle(previous_index, index, 0)
        route_distance += distance_routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(labels[manager.IndexToNode(index)])
    plan_output += 'Route distance: {}miles\n'.format(route_distance)
    plan_output += 'Route duration: {}'.format(datetime.timedelta(seconds=route_duration))
    print(plan_output)

def main():
    """Entry point of the program."""
    addresses, labels = receive_input()

    # Create the data.
    data = create_data(addresses)
    API_key = data['API_key']
    distance_matrix, duration_matrix = create_distance_duration_matrix(data)

    # Instantiate the data problem.
    data = create_data_model(distance_matrix, duration_matrix)

    ##### DISTANCE #####
    # Create the distance routing index manager.
    distance_manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Distance Routing Model.
    distance_routing = pywrapcp.RoutingModel(distance_manager)

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = distance_manager.IndexToNode(from_index)
        to_node = distance_manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    distance_transit_callback_index = distance_routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    distance_routing.SetArcCostEvaluatorOfAllVehicles(distance_transit_callback_index)

    ##### Duration #####
    # Create the distance routing index manager.
    duration_manager = pywrapcp.RoutingIndexManager(len(data['duration_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Distance Routing Model.
    duration_routing = pywrapcp.RoutingModel(duration_manager)

    def duration_callback(from_index, to_index):
        """Returns the time between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = duration_manager.IndexToNode(from_index)
        to_node = duration_manager.IndexToNode(to_index)
        return data['duration_matrix'][from_node][to_node]

    duration_transit_callback_index = duration_routing.RegisterTransitCallback(duration_callback)

    # Define cost of each arc.
    duration_routing.SetArcCostEvaluatorOfAllVehicles(duration_transit_callback_index)

    ##########

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    distance_solution = distance_routing.SolveWithParameters(search_parameters)
    duration_solution = duration_routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if distance_solution:
        print_distance_solution(distance_manager, distance_routing, duration_routing, distance_solution, labels)
    if duration_solution:
      print_duration_solution(duration_manager, duration_routing, distance_routing, duration_solution, labels)


if __name__ == '__main__':
    main()