"""
CCS 2226 Foundations of AI - 2026
Task Two – Constraint Satisfaction Program
(a) Map colouring for Australia (5 regions, 3 colours: Blue, Red, Green)
(b) Map colouring for Nairobi's 17 sub-counties (minimum colours)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

# ═══════════════════════════════════════════════════════════
# Helper: Backtracking CSP Solver
# ═══════════════════════════════════════════════════════════

def is_consistent(region, colour, assignment, neighbours):
    """Return True if assigning `colour` to `region` breaks no constraints."""
    for neighbour in neighbours.get(region, []):
        if assignment.get(neighbour) == colour:
            return False
    return True


def backtrack(regions, colours, neighbours, assignment=None):
    """
    Recursive backtracking search.
    Returns a complete assignment {region: colour} or None if unsolvable.
    """
    if assignment is None:
        assignment = {}

    # All regions assigned → solution found
    if len(assignment) == len(regions):
        return assignment

    # Select next unassigned region (simple order)
    unassigned = [r for r in regions if r not in assignment]
    region = unassigned[0]

    for colour in colours:
        if is_consistent(region, colour, assignment, neighbours):
            assignment[region] = colour
            result = backtrack(regions, colours, neighbours, assignment)
            if result is not None:
                return result
            del assignment[region]          # backtrack

    return None                             # trigger backtrack


# ═══════════════════════════════════════════════════════════
# (a) AUSTRALIA MAP COLOURING
# ═══════════════════════════════════════════════════════════
print("=" * 55)
print("(a) Australia Map Colouring Constraint Satisfaction")
print("=" * 55)

# Five mainland regions + Tasmania (island – no land neighbours)
australia_regions = ["WA", "NT", "SA", "QLD", "NSW", "VIC"]

australia_neighbours = {
    "WA":  ["NT", "SA"],
    "NT":  ["WA", "SA", "QLD"],
    "SA":  ["WA", "NT", "QLD", "NSW", "VIC"],
    "QLD": ["NT", "SA", "NSW"],
    "NSW": ["SA", "QLD", "VIC"],
    "VIC": ["SA", "NSW"],
}

australia_colours = ["Blue", "Red", "Green"]

solution_aus = backtrack(australia_regions, australia_colours, australia_neighbours)

print("\nAustralia Colouring Solution:")
for region, colour in solution_aus.items():
    print(f"  {region:4s} → {colour}")

# ── Visualise with a graph diagram ──
G_aus = nx.Graph()
G_aus.add_nodes_from(australia_regions)
for region, nbrs in australia_neighbours.items():
    for nbr in nbrs:
        G_aus.add_edge(region, nbr)

colour_map_aus = {
    "Blue":  "#4C9BE8",
    "Red":   "#E85C5C",
    "Green": "#4CAF50",
}
node_colours_aus = [colour_map_aus[solution_aus[n]] for n in G_aus.nodes()]

pos_aus = {
    "WA":  (0, 1), "NT":  (2, 2), "SA":  (2, 0),
    "QLD": (4, 2), "NSW": (4, 0), "VIC": (3.5, -1.5),
}

fig1, ax1 = plt.subplots(figsize=(9, 5))
nx.draw_networkx(
    G_aus, pos=pos_aus, ax=ax1,
    node_color=node_colours_aus, node_size=2000,
    font_color="white", font_weight="bold", font_size=12,
    edge_color="#555", width=2,
)
legend_patches = [mpatches.Patch(color=v, label=k) for k, v in colour_map_aus.items()]
ax1.legend(handles=legend_patches, loc="lower right", fontsize=11)
ax1.set_title("(a) Australia Map Colouring – CSP Solution\n"
              "No two adjacent regions share the same colour",
              fontsize=13, fontweight="bold")
ax1.axis("off")
plt.tight_layout()
plt.savefig("australia_colouring.png", dpi=130)
print("\nAustralia graph saved → australia_colouring.png")


# ═══════════════════════════════════════════════════════════
# (b) NAIROBI SUB-COUNTIES MAP COLOURING (minimum colours)
# ═══════════════════════════════════════════════════════════
print("\n" + "=" * 55)
print("(b) Nairobi Sub-County Colouring (Minimum Colours)")
print("=" * 55)

# Nairobi's 17 sub-counties with adjacency relationships
nairobi_regions = [
    "Westlands", "Dagoretti North", "Dagoretti South",
    "Langata", "Kibra", "Roysambu", "Kasarani",
    "Ruaraka", "Embakasi South", "Embakasi North",
    "Embakasi Central", "Embakasi East", "Embakasi West",
    "Makadara", "Kamukunji", "Starehe", "Mathare",
]

nairobi_neighbours = {
    "Westlands":        ["Dagoretti North", "Roysambu", "Starehe", "Kamukunji"],
    "Dagoretti North":  ["Westlands", "Dagoretti South", "Kibra", "Starehe"],
    "Dagoretti South":  ["Dagoretti North", "Langata", "Kibra"],
    "Langata":          ["Dagoretti South", "Kibra", "Embakasi West"],
    "Kibra":            ["Dagoretti North", "Dagoretti South", "Langata",
                         "Embakasi West", "Makadara"],
    "Roysambu":         ["Westlands", "Kasarani", "Ruaraka", "Starehe"],
    "Kasarani":         ["Roysambu", "Ruaraka", "Embakasi North", "Mathare"],
    "Ruaraka":          ["Roysambu", "Kasarani", "Embakasi North",
                         "Makadara", "Mathare"],
    "Embakasi South":   ["Embakasi Central", "Embakasi East", "Embakasi West"],
    "Embakasi North":   ["Kasarani", "Ruaraka", "Embakasi Central",
                         "Embakasi East", "Makadara"],
    "Embakasi Central": ["Embakasi North", "Embakasi South", "Embakasi East",
                         "Embakasi West", "Makadara"],
    "Embakasi East":    ["Embakasi North", "Embakasi South", "Embakasi Central"],
    "Embakasi West":    ["Langata", "Kibra", "Embakasi South", "Embakasi Central",
                         "Makadara"],
    "Makadara":         ["Kibra", "Ruaraka", "Embakasi North", "Embakasi Central",
                         "Embakasi West", "Kamukunji", "Starehe"],
    "Kamukunji":        ["Westlands", "Dagoretti North", "Makadara",
                         "Starehe", "Mathare"],
    "Starehe":          ["Westlands", "Dagoretti North", "Roysambu",
                         "Makadara", "Kamukunji", "Mathare"],
    "Mathare":          ["Kasarani", "Ruaraka", "Kamukunji", "Starehe"],
}

# Try minimum number of colours starting from 3 (Four-Colour Theorem guarantees ≤4)
solution_nbr = None
colours_used  = 0
for num_colours in range(3, 6):
    palette = [f"C{i}" for i in range(num_colours)]
    result  = backtrack(nairobi_regions, palette, nairobi_neighbours)
    if result is not None:
        solution_nbr = result
        colours_used  = num_colours
        break

print(f"\nMinimum colours needed: {colours_used}")
print("\nNairobi Sub-County Colouring Solution:")
for region, colour in solution_nbr.items():
    print(f"  {region:20s} → Colour {colour}")

# ── Visualise Nairobi as a graph ──
G_nbr = nx.Graph()
G_nbr.add_nodes_from(nairobi_regions)
for region, nbrs in nairobi_neighbours.items():
    for nbr in nbrs:
        G_nbr.add_edge(region, nbr)

# Assign distinct display colours per colour index
display_palette = {
    "C0": "#4C9BE8",   # Blue
    "C1": "#E85C5C",   # Red
    "C2": "#4CAF50",   # Green
    "C3": "#F4A742",   # Orange (if needed)
    "C4": "#9B59B6",   # Purple (if needed)
}
label_palette = {
    "C0": "Blue", "C1": "Red", "C2": "Green",
    "C3": "Orange", "C4": "Purple",
}

node_colours_nbr = [display_palette[solution_nbr[n]] for n in G_nbr.nodes()]

pos_nbr = nx.spring_layout(G_nbr, seed=7, k=2.2)

fig2, ax2 = plt.subplots(figsize=(14, 9))
nx.draw_networkx(
    G_nbr, pos=pos_nbr, ax=ax2,
    node_color=node_colours_nbr, node_size=1800,
    font_color="white", font_weight="bold", font_size=7.5,
    edge_color="#777", width=1.5,
)
used_colours = sorted(set(solution_nbr.values()))
legend_patches = [
    mpatches.Patch(color=display_palette[c], label=label_palette[c])
    for c in used_colours
]
ax2.legend(handles=legend_patches, loc="upper right", fontsize=12,
           title="Colours Used", title_fontsize=12)
ax2.set_title(
    f"(b) Nairobi Sub-County Colouring – CSP Solution\n"
    f"17 Sub-Counties coloured with {colours_used} colours (minimum)\n"
    "No two adjacent sub-counties share the same colour",
    fontsize=12, fontweight="bold",
)
ax2.axis("off")
plt.tight_layout()
plt.savefig("nairobi_colouring.png", dpi=130)
print("\nNairobi graph saved → nairobi_colouring.png")
print("\nTask Two complete!")
