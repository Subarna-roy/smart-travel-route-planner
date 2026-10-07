# Smart Travel Route & Trip Planner

A customer-friendly Python DAA mini project for planning tourist visits and travel routes.

## What the customer can do

- Find a tourist place
- See top-rated places
- Find the shortest route between cities
- Find attractions within a budget
- Plan sightseeing according to available time
- Generate possible trip plans
- Explore connected cities
- Read a simple explanation of how the system works

## DAA algorithms used behind the interface

| DAA Topic | Algorithm | Purpose |
|---|---|---|
| Searching | Linear Search | Find a tourist place |
| Searching | Binary Search | Fast search demonstration |
| Sorting | Bubble Sort | Rating comparison |
| Divide & Conquer | Merge Sort | Rank tourist places |
| Divide & Conquer | Quick Sort | Rank tourist places |
| Greedy | Greedy selection | Fit attractions into available time |
| Dynamic Programming | 0/1 Knapsack | Best attractions within budget |
| Graph | BFS | Explore connected cities |
| Graph | DFS | Graph traversal |
| Graph | Dijkstra | Shortest travel route |
| Backtracking | Backtracking | Generate possible trip plans |
| Complexity | Big-O | Analyze algorithm performance |

## Run in VS Code

1. Extract the ZIP.
2. Open the `Smart_Travel_Route_Trip_Planner` folder in VS Code.
3. Open **Terminal -> New Terminal**.
4. Run:

```bash
python main.py
```

On Windows, if needed:

```bash
py main.py
```

No external Python packages are required.

## Files

```text
main.py
places.csv
routes.csv
README.md
sample_output.txt
.gitignore
```

## Important project explanation

The customer does not need to know algorithm names. They simply choose travel options and provide understandable information such as:

- destination
- budget
- available sightseeing time
- number of places

The DAA algorithms operate behind the scenes to produce the results.

## Project scope

This is an educational project using a small sample dataset. It does not use live maps, live traffic, hotel APIs, or real-time prices.

## Future improvements

- GUI or web interface
- Google Maps or OpenStreetMap integration
- Live traffic
- Hotel and transport booking
- Weather information
- Larger destination database
- User accounts and saved trips
