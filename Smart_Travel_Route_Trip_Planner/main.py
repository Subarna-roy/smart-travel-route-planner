"""
Smart Travel Route & Trip Planner
Customer-friendly DAA Mini Project
"""

import csv


# ---------------- DATA ----------------

def load_places(filename):
    places = []
    with open(filename, "r", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            row["cost"] = int(row["cost"])
            row["rating"] = float(row["rating"])
            row["time"] = int(row["time"])
            places.append(row)
    return places


def load_routes(filename):
    routes = []
    with open(filename, "r", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            routes.append(
                (row["source"], row["destination"], int(row["distance"]))
            )
    return routes


# ---------------- SEARCHING ----------------

def linear_search(places, name):
    # O(n)
    for place in places:
        if place["name"].lower() == name.lower():
            return place
    return None


def binary_search(places, name):
    # O(log n)
    data = sorted(places, key=lambda x: x["name"].lower())
    left, right = 0, len(data) - 1

    while left <= right:
        mid = (left + right) // 2
        current = data[mid]["name"].lower()

        if current == name.lower():
            return data[mid]
        if current < name.lower():
            left = mid + 1
        else:
            right = mid - 1

    return None


# ---------------- SORTING ----------------

def bubble_sort(places):
    # O(n^2)
    data = places[:]
    for i in range(len(data)):
        for j in range(0, len(data) - i - 1):
            if data[j]["rating"] < data[j + 1]["rating"]:
                data[j], data[j + 1] = data[j + 1], data[j]
    return data


def merge_sort(places):
    # O(n log n)
    if len(places) <= 1:
        return places

    mid = len(places) // 2
    left = merge_sort(places[:mid])
    right = merge_sort(places[mid:])

    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i]["rating"] >= right[j]["rating"]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    return result + left[i:] + right[j:]


def quick_sort(places):
    # Average O(n log n)
    if len(places) <= 1:
        return places

    pivot = places[-1]["rating"]
    high = [p for p in places[:-1] if p["rating"] >= pivot]
    low = [p for p in places[:-1] if p["rating"] < pivot]

    return quick_sort(high) + [places[-1]] + quick_sort(low)


# ---------------- GRAPH ----------------

def build_graph(routes):
    graph = {}
    for source, destination, distance in routes:
        graph.setdefault(source, []).append((destination, distance))
        graph.setdefault(destination, []).append((source, distance))
    return graph


def bfs(graph, start):
    # O(V + E)
    visited = set()
    queue = [start]
    order = []

    while queue:
        current = queue.pop(0)
        if current in visited:
            continue

        visited.add(current)
        order.append(current)

        for neighbor, _ in graph.get(current, []):
            if neighbor not in visited:
                queue.append(neighbor)

    return order


def dfs(graph, start):
    # O(V + E)
    visited = set()
    order = []

    def visit(node):
        visited.add(node)
        order.append(node)
        for neighbor, _ in graph.get(node, []):
            if neighbor not in visited:
                visit(neighbor)

    visit(start)
    return order


def dijkstra(graph, start, destination):
    # O(V^2) for this implementation
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}
    remaining = set(graph)

    distances[start] = 0

    while remaining:
        current = min(remaining, key=lambda x: distances[x])

        if distances[current] == float("inf"):
            break

        remaining.remove(current)

        if current == destination:
            break

        for neighbor, distance in graph[current]:
            new_distance = distances[current] + distance

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current

    if distances.get(destination, float("inf")) == float("inf"):
        return None, []

    path = []
    current = destination

    while current is not None:
        path.append(current)
        current = previous[current]

    return distances[destination], path[::-1]


# ---------------- GREEDY ----------------

def best_day_plan(places, hours):
    # Greedy: choose shorter attractions first.
    selected = []
    used = 0

    for place in sorted(places, key=lambda x: x["time"]):
        if used + place["time"] <= hours:
            selected.append(place)
            used += place["time"]

    return selected


# ---------------- DYNAMIC PROGRAMMING ----------------

def best_budget_plan(places, budget):
    # 0/1 Knapsack: O(n * budget)
    n = len(places)
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        cost = places[i - 1]["cost"]
        value = int(places[i - 1]["rating"] * 10)

        for money in range(budget + 1):
            dp[i][money] = dp[i - 1][money]

            if cost <= money:
                dp[i][money] = max(
                    dp[i][money],
                    value + dp[i - 1][money - cost]
                )

    selected = []
    money = budget

    for i in range(n, 0, -1):
        if dp[i][money] != dp[i - 1][money]:
            selected.append(places[i - 1])
            money -= places[i - 1]["cost"]

    return selected[::-1]


# ---------------- BACKTRACKING ----------------

def make_itineraries(places, max_places, budget, limit=5):
    results = []

    def backtrack(start, chosen, cost):
        if len(results) >= limit:
            return

        if chosen:
            results.append((chosen[:], cost))

        if len(chosen) == max_places:
            return

        for i in range(start, len(places)):
            place = places[i]

            if cost + place["cost"] <= budget:
                chosen.append(place)
                backtrack(i + 1, chosen, cost + place["cost"])
                chosen.pop()

    backtrack(0, [], 0)
    return results


# ---------------- DISPLAY HELPERS ----------------

def show_place(place):
    print(f"""
Place       : {place['name']}
City        : {place['city']}
Approx. Cost: ₹{place['cost']}
Rating      : {place['rating']}/5
Visit Time  : {place['time']} hours
""")


def show_places(places):
    print("\nRecommended Places")
    print("-" * 65)

    for number, place in enumerate(places, 1):
        print(
            f"{number}. {place['name']} ({place['city']}) "
            f"- ₹{place['cost']} - {place['rating']}/5 - {place['time']} hrs"
        )

    print("-" * 65)


def choose_city(graph, message):
    cities = sorted(graph.keys())

    print("\nAvailable cities:")
    for i, city in enumerate(cities, 1):
        print(f"{i}. {city}")

    value = input(f"\n{message} ").strip()

    if value.isdigit() and 1 <= int(value) <= len(cities):
        return cities[int(value) - 1]

    for city in cities:
        if city.lower() == value.lower():
            return city

    print("Sorry, I couldn't find that city.")
    return None


# ---------------- MAIN CUSTOMER INTERFACE ----------------

def main():
    places = load_places("places.csv")
    routes = load_routes("routes.csv")
    graph = build_graph(routes)

    while True:
        print("\n" + "=" * 60)
        print("        SMART TRAVEL ROUTE & TRIP PLANNER")
        print("=" * 60)
        print("Welcome! Let's help you plan your trip.")
        print("""
1. Find a tourist place
2. See top-rated places
3. Find the best route between two cities
4. Find the best places for my budget
5. Plan places for my available time
6. Create possible trip plans
7. Explore nearby connected cities
8. View how the planner works
0. Exit
""")

        choice = input("What would you like to do? Enter a number: ").strip()

        if choice == "1":
            print("\nYou can search for places such as:")
            print("Rock Garden, Golden Temple, Taj Mahal, India Gate...")

            name = input("\nEnter the tourist place name: ").strip()

            result = linear_search(places, name)

            if result:
                print("\nWe found your place!")
                show_place(result)
            else:
                print("\nSorry, that tourist place is not in our sample list.")

        elif choice == "2":
            print("\nHere are the highest-rated tourist places:")
            result = merge_sort(places)[:7]
            show_places(result)

        elif choice == "3":
            print("\nLet's find the shortest travel route for you.")

            source = choose_city(graph, "Choose your starting city:")
            if not source:
                continue

            destination = choose_city(graph, "Choose your destination city:")
            if not destination:
                continue

            if source == destination:
                print("\nYou are already in that city!")
                continue

            distance, path = dijkstra(graph, source, destination)

            if path:
                print("\nYour shortest route is:")
                print(" → ".join(path))
                print(f"Approximate distance: {distance} km")
            else:
                print("\nSorry, no route was found.")

        elif choice == "4":
            try:
                budget = int(input("\nWhat is your maximum budget? ₹"))

                if budget <= 0:
                    print("Please enter a budget greater than ₹0.")
                    continue

                result = best_budget_plan(places, budget)

                if result:
                    print(f"\nBest places we found within ₹{budget}:")
                    show_places(result)
                    print(
                        f"Estimated total cost: ₹"
                        f"{sum(p['cost'] for p in result)}"
                    )
                else:
                    print("\nNo place fits within that budget.")

            except ValueError:
                print("\nPlease enter the budget as a number, for example 3000.")

        elif choice == "5":
            try:
                hours = int(input("\nHow many hours do you have for sightseeing? "))

                if hours <= 0:
                    print("Please enter at least 1 hour.")
                    continue

                result = best_day_plan(places, hours)

                print(f"\nHere is a plan that fits within {hours} hours:")
                show_places(result)
                print(f"Total sightseeing time: {sum(p['time'] for p in result)} hours")

            except ValueError:
                print("\nPlease enter the time as a number, for example 8.")

        elif choice == "6":
            try:
                max_places = int(
                    input("\nHow many places would you like to visit? ")
                )
                budget = int(input("What is your maximum budget? ₹"))

                if max_places <= 0 or budget <= 0:
                    print("Please enter positive numbers.")
                    continue

                plans = make_itineraries(places, max_places, budget)

                if not plans:
                    print("\nSorry, no trip plan matched your requirements.")
                else:
                    print("\nHere are some possible trip plans:")

                    for number, (plan, cost) in enumerate(plans, 1):
                        names = " → ".join(p["name"] for p in plan)
                        print(f"\nPlan {number}")
                        print(names)
                        print(f"Estimated cost: ₹{cost}")

            except ValueError:
                print("\nPlease enter valid numbers.")

        elif choice == "7":
            print("\nChoose a city to explore connected destinations.")

            city = choose_city(graph, "Starting city:")
            if city:
                connected = bfs(graph, city)
                print("\nCities you can explore from there:")
                print(" → ".join(connected))

        elif choice == "8":
            print("""
HOW DOES THE TRAVEL PLANNER WORK?

Behind the simple customer interface, the project uses
different DAA algorithms:

• Searching
  Finds tourist places quickly.

• Sorting
  Ranks places by rating.

• Dijkstra's Algorithm
  Finds the shortest route between cities.

• BFS and DFS
  Explore connected cities.

• Greedy Algorithm
  Selects attractions that fit your available time.

• Dynamic Programming
  Selects the best attractions within your budget.

• Backtracking
  Creates different possible trip plans.

This makes the application practical while demonstrating
major Design and Analysis of Algorithms concepts.
""")

        elif choice == "0":
            print("\nThank you for using Smart Travel Planner!")
            print("Have a safe and enjoyable trip. ✈️")
            break

        else:
            print("\nPlease choose one of the options from 0 to 8.")


if __name__ == "__main__":
    main()
