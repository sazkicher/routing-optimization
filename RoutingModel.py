"""
Capacited Vehicles Routing Problem (CVRP) - Using OR Tools.

"""
import json
from datetime import datetime

from ortools.constraint_solver import pywrapcp, routing_enums_pb2

from matrixRoutes import matrixRoutes_main


def create_data_model():
    """Stores the data for the problem."""
    
    x = matrixRoutes_main()
    data = json.loads(x)
    #data = {}
    #data['distance_matrix'] = [[0, 7624, 4087, 19106, 3724, 13765, 14369, 11553, 7927, 12952, 8277], [7458, 0, 6930, 13160, 8125, 15000, 15873, 12802, 10873, 21714, 8886], [4221, 5317, 0, 15586, 3331, 13848, 14721, 11650, 7877, 19398, 9285], [18638, 12390, 16618, 0, 16034, 15319, 15705, 13675, 16160, 32184, 20170], [3620, 8323, 1971, 16493, 0, 11120, 11724, 8908, 5282, 16162, 10042], [14572, 15426, 12922, 15646,11949, 0, 6155, 2414, 10214, 27114, 20940], [14880, 15734, 13230, 15954, 12257, 6297, 0, 4653, 10522, 27422, 21248], [12417, 12992, 10767, 14013, 9794, 2472, 4522, 0, 8059, 29432, 18506], [8430, 11322, 6780, 16585, 5807, 9737, 10341, 7525, 0, 20972, 15230], [11379, 18067, 15231, 29906, 14167, 24208, 29040, 21996, 18370, 0, 13118], [10167, 9959, 9629, 19118, 12677, 20985, 21858, 18787, 16880, 16291, 0]]
    #data['demands'] = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    #data['vehicle_capacities'] = [4, 4, 4, 4, 4, 4]
    #data['num_vehicles'] = 6
    #data['depot'] = 0
    return data


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    #print(f'Objective: {solution.ObjectiveValue()}')
    total_distance = 0
    total_load = 0
    testarray2 = []
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        testarray = []
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
            #testarray.append(node_index)
            testarray.append(data["Addresses"][node_index][0])
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += ' {0} Load({1})\n'.format(manager.IndexToNode(index),
                                                 route_load)
        testarray.append(manager.IndexToNode(index))
        testarray.append(route_distance/1000)
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        plan_output += 'Load of the route: {}\n'.format(route_load)
        #print(plan_output)
        testarray.remove(0)
        #testarray.remove(0)
        # print(testarray)
        testarray2.append(testarray)
        total_distance += route_distance
        total_load += route_load
        testarray2 = [sub for sub in testarray2 if len(sub) >= 3]
    print('Total distance of all routes: {} km'.format(total_distance/1000))
    #print('Total load of all routes: {}'.format(total_load))
    answer = json.dumps(testarray2)
    print(f"Number of created routes: {len(testarray2)}")
    print(f"Vehicle occupation: {round((data['num_vehicles']-1)/len(testarray2),2)}")
    print(f"Route groups: {answer}")


def main():
    """Solve the CVRP problem."""
    # Instantiate the data problem.
    data = create_data_model()
    # print(data)
    # Create the routing index manager.
    print("Starting routing model.")
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])
    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)
    # Create and register a transit callback.

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    # Add Capacity constraint.

    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]
    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

# Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        data['max_distance'],  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    #print(data['max_distance'])
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.FromSeconds(15) # ---- time to think ----
    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)
    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)
        # print(json.dumps(sys.argv[1]))
    else:
        print("sin solucion")

    now = datetime.now()
    print(f"End at: {now}")
if __name__ == '__main__':
    main()
