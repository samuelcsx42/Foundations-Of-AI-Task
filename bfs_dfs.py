"""
=============================================================
  Task Four – Search and Optimization
  Breadth-First Search (BFS) and Depth-First Search (DFS)
  with annotated search-path output.

  Graph used (undirected adjacency list):

        A
       / \
      B   C
     / \   \
    D   E   F
         \
          G  ← GOAL

  Run: python bfs_dfs.py
=============================================================
"""

from collections import deque   # deque gives O(1) popleft for BFS queue


# ─────────────────────────────────────────────────────────────
#  GRAPH DEFINITION
#  An undirected graph represented as an adjacency list.
#  Keys are nodes; values are lists of neighbour nodes.
# ─────────────────────────────────────────────────────────────
GRAPH = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'G'],
    'F': ['C'],
    'G': ['E'],   # G is our goal node
}


# ─────────────────────────────────────────────────────────────
#  HELPER: print_path
#  Pretty-prints the search path as:  A → B → E → G
# ─────────────────────────────────────────────────────────────
def print_path(path: list[str]) -> None:
    print("  Path:", " → ".join(path))


# =============================================================
#  BREADTH-FIRST SEARCH (BFS)
#
#  Strategy : Explore all neighbours at the current depth
#             before moving one level deeper (level-order).
#  Data structure: FIFO Queue  (collections.deque)
#  Guarantees  : Shortest path in an unweighted graph.
#  Time  complexity: O(V + E)
#  Space complexity: O(V)  – visited set + queue
# =============================================================
def bfs(graph: dict, start: str, goal: str) -> list[str] | None:
    """
    Perform Breadth-First Search.

    Parameters
    ----------
    graph : dict   – adjacency list
    start : str    – starting node
    goal  : str    – target node

    Returns
    -------
    list[str] | None – ordered path from start → goal,
                       or None if no path exists.
    """

    print("\n" + "=" * 55)
    print("  BREADTH-FIRST SEARCH (BFS)")
    print(f"  Start: {start}  |  Goal: {goal}")
    print("=" * 55)

    # visited keeps track of already-explored nodes
    visited: set[str] = set()

    # The queue holds (current_node, path_so_far) pairs.
    # We initialise it with the start node.
    queue: deque = deque([(start, [start])])

    step = 1   # step counter for display

    while queue:
        # Dequeue the front element (FIFO order)
        current_node, path = queue.popleft()

        print(f"\n  Step {step}: Visiting node '{current_node}'")
        print(f"           Current path: {' → '.join(path)}")
        step += 1

        # ── GOAL CHECK ──────────────────────────────────────
        if current_node == goal:
            print(f"\n  ✔ Goal '{goal}' FOUND!")
            print_path(path)
            return path

        # ── MARK AS VISITED ─────────────────────────────────
        if current_node in visited:
            print(f"           (already visited — skipping)")
            continue
        visited.add(current_node)

        # ── EXPAND NEIGHBOURS ───────────────────────────────
        neighbours = graph.get(current_node, [])
        print(f"           Neighbours: {neighbours}")

        for neighbour in neighbours:
            if neighbour not in visited:
                # Enqueue each unvisited neighbour with the
                # extended path (append neighbour to copy of path)
                queue.append((neighbour, path + [neighbour]))
                print(f"           → Enqueued '{neighbour}'")

    # If the queue empties without finding the goal
    print(f"\n  ✘ Goal '{goal}' NOT reachable from '{start}'.")
    return None


# =============================================================
#  DEPTH-FIRST SEARCH (DFS)
#
#  Strategy : Go as deep as possible along one branch before
#             backtracking and exploring other branches.
#  Data structure: LIFO Stack  (Python list used as stack)
#  Does NOT guarantee: shortest path.
#  Time  complexity: O(V + E)
#  Space complexity: O(V)
# =============================================================
def dfs(graph: dict, start: str, goal: str) -> list[str] | None:
    """
    Perform Depth-First Search.

    Parameters
    ----------
    graph : dict   – adjacency list
    start : str    – starting node
    goal  : str    – target node

    Returns
    -------
    list[str] | None – ordered path from start → goal,
                       or None if no path exists.
    """

    print("\n" + "=" * 55)
    print("  DEPTH-FIRST SEARCH (DFS)")
    print(f"  Start: {start}  |  Goal: {goal}")
    print("=" * 55)

    # visited tracks nodes already fully explored
    visited: set[str] = set()

    # The stack holds (current_node, path_so_far) pairs.
    # We use Python's list: append() = push, pop() = pop.
    stack: list = [(start, [start])]

    step = 1

    while stack:
        # Pop the TOP element (LIFO order — goes deep first)
        current_node, path = stack.pop()

        print(f"\n  Step {step}: Visiting node '{current_node}'")
        print(f"           Current path: {' → '.join(path)}")
        step += 1

        # ── GOAL CHECK ──────────────────────────────────────
        if current_node == goal:
            print(f"\n  ✔ Goal '{goal}' FOUND!")
            print_path(path)
            return path

        # ── SKIP IF ALREADY VISITED ─────────────────────────
        if current_node in visited:
            print(f"           (already visited — skipping)")
            continue
        visited.add(current_node)

        # ── EXPAND NEIGHBOURS ───────────────────────────────
        neighbours = graph.get(current_node, [])
        # Reverse so that the first neighbour in the list is
        # explored first (top of stack = first neighbour).
        print(f"           Neighbours: {neighbours}")

        for neighbour in reversed(neighbours):
            if neighbour not in visited:
                stack.append((neighbour, path + [neighbour]))
                print(f"           → Pushed  '{neighbour}'")

    # Stack exhausted without reaching goal
    print(f"\n  ✘ Goal '{goal}' NOT reachable from '{start}'.")
    return None


# =============================================================
#  MAIN — Run both algorithms on the same graph
# =============================================================
if __name__ == "__main__":

    START = 'A'
    GOAL  = 'G'

    print("\n╔═══════════════════════════════════════════════════╗")
    print("║   Task Four: BFS & DFS — Search Path Demo         ║")
    print("╚═══════════════════════════════════════════════════╝")

    print("""
  Graph layout:
        A
       / \\
      B   C
     / \\   \\
    D   E   F
         \\
          G  ← GOAL
    """)

    # ── Run BFS ───────────────────────────────────────────────
    bfs_result = bfs(GRAPH, START, GOAL)

    # ── Run DFS ───────────────────────────────────────────────
    dfs_result = dfs(GRAPH, START, GOAL)

    # ── Summary ───────────────────────────────────────────────
    print("\n" + "=" * 55)
    print("  SUMMARY")
    print("=" * 55)
    if bfs_result:
        print(f"  BFS path ({len(bfs_result)-1} steps): {' → '.join(bfs_result)}")
    if dfs_result:
        print(f"  DFS path ({len(dfs_result)-1} steps): {' → '.join(dfs_result)}")

    print("""
  Key differences:
  ┌──────────────┬──────────────────────┬────────────────────┐
  │              │  BFS                 │  DFS               │
  ├──────────────┼──────────────────────┼────────────────────┤
  │ Structure    │  Queue (FIFO)        │  Stack (LIFO)      │
  │ Explores     │  Level by level      │  Branch by branch  │
  │ Shortest?    │  Yes (unweighted)    │  Not guaranteed    │
  │ Memory use   │  Higher              │  Lower             │
  │ Best for     │  Shortest path       │  Deep/maze graphs  │
  └──────────────┴──────────────────────┴────────────────────┘
    """)
