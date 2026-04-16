# Route Planning System with Pseudocode

import heapq
from pathlib import Path


# Function 0: Load route data from a text file
# --------------------------------------------
# Define function load_route_data(filenam)
#     Initialize empty list route_data
#     Open the file with route information
#     For each line :
#         Split the line into starting city, destination city, and distance
#         Convert distance from text to an integer
#         Store the route details in a dictionary
#     Return the list of route diocst
def load_route_data(filename):
    route_data = []
    file_path = Path(filename)

    with file_path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            starting_point, destination, distance = [
                part.strip() for part in line.split(",")
            ]
            route_data.append(
                {
                    "starting_point": starting_point,
                    "destination": destination,
                    "distance": int(distance),
                }
            )

    return route_data

# Function 1: Fully written in pseudocode
# ----------------------------------------
# Define function process_route_data(data)
#     Initialize empty dictionary route_map
#     For each entry in data:
#         Extract 'starting_point', 'destination', and 'distance'
#         Store 'starting_point' as key and a list of (dest, dist) tuples as value in route_map
#     Return route_map
def process_route_data(data):
    route_map = {}

    for entry in data:
        starting_point = entry["starting_point"]
        destination = entry["destination"]
        distance = entry["distance"]

        if starting_point not in route_map:
            route_map[starting_point] = []
        if destination not in route_map:
            route_map[destination] = []

        route_map[starting_point].append((destination, distance))
        route_map[destination].append((starting_point, distance))

    return route_map


# Function 2: Function header with brief pseudocode
# --------------------------------------------------
def find_shortest_route(start, destination, route_map):
    """
    Find the shortest route between two locations.
    - Use a pathfinding algorithm to determine the optimal route.
    - Return the route and estimated distance.
    """
    if start not in route_map or destination not in route_map:
        return None

    priority_queue = [(0, start, [start])]
    visited = set()

    while priority_queue:
        current_distance, current_city, path = heapq.heappop(priority_queue)

        if current_city == destination:
            return path, current_distance

        if current_city in visited:
            continue

        visited.add(current_city)

        for next_city, distance in route_map[current_city]:
            if next_city not in visited:
                heapq.heappush(
                    priority_queue,
                    (current_distance + distance, next_city, path + [next_city]),
                )

    return None

# Pseudocode block 1: No function title, just high-level steps
# ------------------------------------------------------------
# Read user input for starting location and destination
# Validate that both locations exist in the route map
# If both are valid, call the shortest route function and return the result
# If not, return an error message
def plan_single_route(route_map):
    try:
        start = input("Enter starting location: ").strip()
    except EOFError:
        return False

    if start.lower() == "quit":
        return False

    try:
        destination = input("Enter destination: ").strip()
    except EOFError:
        return False

    if destination.lower() == "quit":
        return False

    if start not in route_map:
        print(f"Error: '{start}' is not in the route map.")
        return True

    if destination not in route_map:
        print(f"Error: '{destination}' is not in the route map.")
        return True

    result = find_shortest_route(start, destination, route_map)
    if result is None:
        print(f"No route found from {start} to {destination}.")
        return True

    route, distance = result
    print(f"Shortest route: {' -> '.join(route)}")
    print(f"Distance: {distance} miles")
    return True

# Pseudocode block 2: Another missing function title
# --------------------------------------------------
# Allow the system to handle multiple route calculations in a loop
# - Continue accepting input from the user
# - Provide the shortest route for each query
# - Allow the user to exit by typing 'quit'
def route_planning_loop(route_map):
    print("Route Planning System")
    print("Type 'quit' as either city to exit.")

    while True:
        should_continue = plan_single_route(route_map)
        if not should_continue:
            print("Goodbye!")
            break
        print()

# BLANK SPACE: Students will continue writing the route planning implementation from here
# - Calculate the estimated travel time based on distance and average speed
# - Implement a function to suggest alternative routes if the shortest route is unavailable
# - Design a function that calculates the total fuel cost for a given route based on fuel efficiency

# Function 5: Estimate travel time
# --------------------------------
# Define function estimate_travel_time(distance, average_speed)
#     Check that average_speed is greater than zero
#     Divide distance by average_speed to get hours
#     Return the estimated number of hours
def estimate_travel_time(distance, average_speed):
    if average_speed <= 0:
        raise ValueError("Average speed must be greater than zero.")
    return round(distance / average_speed, 2)


# Function 6: Suggest alternative routes
# --------------------------------------
# Define function suggest_alternative_routes(start, destination, route_map)
#     Find all reasonable paths from start to destination without revisiting cities
#     Calculate the total distance for each path
#     Sort paths from shortest to longest
#     Remove the shortest route from the list of alternatives
#     Return the remaining routes as alternate options
def suggest_alternative_routes(start, destination, route_map):
    if start not in route_map or destination not in route_map:
        return []

    all_routes = []

    def search_paths(current_city, path, total_distance):
        if current_city == destination:
            all_routes.append((path, total_distance))
            return

        for next_city, distance in route_map[current_city]:
            if next_city not in path:
                search_paths(next_city, path + [next_city], total_distance + distance)

    search_paths(start, [start], 0)
    all_routes.sort(key=lambda route: route[1])

    if len(all_routes) <= 1:
        return []
    return all_routes[1:]


# Function 7: Calculate fuel cost
# -------------------------------
# Define function calculate_fuel_cost(distance, mpg, price_per_gallon)
#     Check that miles per gallon is greater than zero
#     Check that price per gallon is not negative
#     Divide distance by miles per gallon to estimate gallons used
#     Multiply gallons used by price per gallon
#     Return the total estimated fuel cost
def calculate_fuel_cost(distance, mpg, price_per_gallon):
    if mpg <= 0:
        raise ValueError("Miles per gallon must be greater than zero.")
    if price_per_gallon < 0:
        raise ValueError("Price per gallon cannot be negative.")

    gallons_used = distance / mpg
    return round(gallons_used * price_per_gallon, 2)

if __name__ == "__main__":
    routes_file = Path(__file__).with_name("routes.txt")
    route_data = load_route_data(routes_file)
    route_map = process_route_data(route_data)
    route_planning_loop(route_map)
