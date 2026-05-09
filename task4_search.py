"""
CCS 2226 Foundations of AI - 2026
Task Four – Search and Optimization
Breadth First Search (BFS) and Depth First Search (DFS)
Both programs output the search path from initial node to goal state.
"""

from collections import deque
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

# ═══════════════════════════════════════════════════════════
# Graph Definition (shared by both BFS and DFS)
# ═══════════════════════════════════════════════════════════
# Adjacency list representing an unweighted undirected graph.

GRAPH = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F", "G"],
    "D": ["B", "H"],
    "E": ["B", "H", "I"],
    "F": ["C", "J"],
    "G": ["C", "J"],
    "H": ["D", "E"],
    "I": ["E", "J"],
    "J": ["F", "G", "I"],   # ← Goal node
}

START = "A"
GOAL  = "J"


# ═══════════════════════════════════════════════════════════
# BREADTH FIRST SEARCH (BFS)
# ═══════════════════════════════════════════════════════════
def bfs(graph, start, goal):
    """
    Breadth First Search – explores nodes level by level.

    Uses a FIFO queue.
    Guarantees the shortest path (fewest edges) in an unweighted graph.

    Parameters
    ----------
    graph : dict  – adjacency list {node: [neighbours]}
    start : str   – starting node
    goal  : str   – target node

    Returns
    -------
    path        : list of nodes from start → goal (or None if unreachable)
    visited_order : list of nodes in the order they were first visited
    """
    # Queue stores (current_node, path_so_far)
    queue         = deque([(start, [start])])
    visited       = {start}         # nodes already added to queue
    visited_order = []              # exploration order log

    print("─" * 50)
    print(f"BFS  |  Start: {start}  →  Goal: {goal}")
    print("─" * 50)

    while queue:
        node, path = queue.popleft()
        visited_order.append(node)
        print(f"  Visiting: {node:2s}  |  Path so far: {' → '.join(path)}")

        # Goal check
        if node == goal:
            print(f"\n  ✔ Goal '{goal}' reached!")
            return path, visited_order

        # Expand neighbours in alphabetical order (consistent exploration)
        for neighbour in sorted(graph[node]):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append((neighbour, path + [neighbour]))

    print(f"\n  ✘ Goal '{goal}' not reachable from '{start}'.")
    return None, visited_order


# ═══════════════════════════════════════════════════════════
# DEPTH FIRST SEARCH (DFS)
# ═══════════════════════════════════════════════════════════
def dfs(graph, start, goal):
    """
    Depth First Search – explores as deep as possible before backtracking.

    Uses a LIFO stack (iterative implementation).
    Does NOT guarantee the shortest path.

    Parameters
    ----------
    graph : dict  – adjacency list {node: [neighbours]}
    start : str   – starting node
    goal  : str   – target node

    Returns
    -------
    path        : list of nodes from start → goal (or None if unreachable)
    visited_order : list of nodes in the order they were first visited
    """
    # Stack stores (current_node, path_so_far)
    stack         = [(start, [start])]
    visited       = set()
    visited_order = []

    print("─" * 50)
    print(f"DFS  |  Start: {start}  →  Goal: {goal}")
    print("─" * 50)

    while stack:
        node, path = stack.pop()

        if node in visited:
            continue                         # skip already-explored nodes

        visited.add(node)
        visited_order.append(node)
        print(f"  Visiting: {node:2s}  |  Path so far: {' → '.join(path)}")

        # Goal check
        if node == goal:
            print(f"\n  ✔ Goal '{goal}' reached!")
            return path, visited_order

        # Push neighbours in reverse-alphabetical order so the
        # alphabetically first neighbour is explored first (stack is LIFO)
        for neighbour in sorted(graph[node], reverse=True):
            if neighbour not in visited:
                stack.append((neighbour, path + [neighbour]))

    print(f"\n  ✘ Goal '{goal}' not reachable from '{start}'.")
    return None, visited_order


# ═══════════════════════════════════════════════════════════
# VISUALISATION HELPER
# ═══════════════════════════════════════════════════════════
def draw_search(graph, path, visited_order, title, ax, pos):
    """Draw the graph highlighting the found path and visited nodes."""
    G = nx.Graph(graph)

    # Node colour coding
    node_colours = []
    for n in G.nodes():
        if n == START:
            node_colours.append("#2196F3")      # blue  – start
        elif n == GOAL:
            node_colours.append("#4CAF50")      # green – goal
        elif n in path:
            node_colours.append("#FF9800")      # orange – on solution path
        elif n in visited_order:
            node_colours.append("#CE93D8")      # purple – visited but off-path
        else:
            node_colours.append("#B0BEC5")      # grey  – not visited

    # Edge colour coding
    path_edges = list(zip(path[:-1], path[1:]))
    edge_colours = []
    for e in G.edges():
        if e in path_edges or (e[1], e[0]) in path_edges:
            edge_colours.append("#E53935")      # red – solution path edges
        else:
            edge_colours.append("#90A4AE")      # grey – other edges

    nx.draw_networkx(
        G, pos=pos, ax=ax,
        node_color=node_colours, edge_color=edge_colours,
        node_size=1400, font_color="white", font_weight="bold", font_size=12,
        width=2.5,
    )

    # Annotate exploration order
    for i, node in enumerate(visited_order):
        x, y = pos[node]
        ax.text(x, y + 0.18, str(i + 1),
                ha="center", va="bottom", fontsize=8,
                color="#333", fontweight="bold")

    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    ax.axis("off")

    # Legend
    legend_items = [
        mpatches.Patch(color="#2196F3", label=f"Start ({START})"),
        mpatches.Patch(color="#4CAF50", label=f"Goal ({GOAL})"),
        mpatches.Patch(color="#FF9800", label="Solution Path"),
        mpatches.Patch(color="#CE93D8", label="Visited (off-path)"),
        mpatches.Patch(color="#E53935", label="Path Edges"),
    ]
    ax.legend(handles=legend_items, loc="lower left", fontsize=8)


# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":

    print("=" * 55)
    print("CCS 2226 Foundations of AI – Task Four")
    print("Search Algorithms: BFS and DFS")
    print(f"Graph nodes : {sorted(GRAPH.keys())}")
    print(f"Start node  : {START}")
    print(f"Goal node   : {GOAL}")
    print("=" * 55)
    print()

    # ── Run BFS ──
    print("BREADTH FIRST SEARCH (BFS)\n")
    bfs_path, bfs_order = bfs(GRAPH, START, GOAL)
    print(f"\n  BFS Solution Path : {' → '.join(bfs_path)}")
    print(f"  Path Length       : {len(bfs_path) - 1} edges")
    print(f"  Nodes Explored    : {len(bfs_order)}")
    print(f"  Exploration Order : {' → '.join(bfs_order)}\n")

    # ── Run DFS ──
    print("\nDEPTH FIRST SEARCH (DFS)\n")
    dfs_path, dfs_order = dfs(GRAPH, START, GOAL)
    print(f"\n  DFS Solution Path : {' → '.join(dfs_path)}")
    print(f"  Path Length       : {len(dfs_path) - 1} edges")
    print(f"  Nodes Explored    : {len(dfs_order)}")
    print(f"  Exploration Order : {' → '.join(dfs_order)}\n")

    # ── Comparison Summary ──
    print("=" * 55)
    print("COMPARISON SUMMARY")
    print("=" * 55)
    print(f"{'Algorithm':<12} {'Path':<30} {'Edges':<8} {'Visited'}")
    print("-" * 55)
    print(f"{'BFS':<12} {' → '.join(bfs_path):<30} {len(bfs_path)-1:<8} {len(bfs_order)}")
    print(f"{'DFS':<12} {' → '.join(dfs_path):<30} {len(dfs_path)-1:<8} {len(dfs_order)}")
    print()
    print("Key differences:")
    print("  BFS : Uses a QUEUE (FIFO) – explores level by level.")
    print("        Guarantees the SHORTEST path in unweighted graphs.")
    print("  DFS : Uses a STACK (LIFO) – dives deep first.")
    print("        Memory efficient; does NOT guarantee shortest path.")

    # ── Visualise ──
    pos = nx.spring_layout(nx.Graph(GRAPH), seed=42)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle(
        f"BFS vs DFS Search  |  Start: {START}  →  Goal: {GOAL}",
        fontsize=15, fontweight="bold",
    )

    draw_search(
        GRAPH, bfs_path, bfs_order,
        f"Breadth First Search (BFS)\nPath: {' → '.join(bfs_path)}  "
        f"({len(bfs_path)-1} edges, {len(bfs_order)} nodes visited)",
        ax1, pos,
    )
    draw_search(
        GRAPH, dfs_path, dfs_order,
        f"Depth First Search (DFS)\nPath: {' → '.join(dfs_path)}  "
        f"({len(dfs_path)-1} edges, {len(dfs_order)} nodes visited)",
        ax2, pos,
    )

    plt.tight_layout()
    plt.savefig("search_bfs_dfs.png", dpi=130)
    print("\nVisualization saved → search_bfs_dfs.png")
    print("\nTask Four complete!")
