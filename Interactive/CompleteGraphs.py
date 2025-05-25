import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.collections import LineCollection
import matplotlib.gridspec as gridspec
from collections import deque
import random


num_vertices = 50 
initial_p = 0.5 
seed = 44
spacing = 2


def generate_Kn(num_vertices):
    # Circle
    angles = np.linspace(0, 2 * np.pi, num_vertices, endpoint=False)
    positions = [(np.cos(angle), np.sin(angle)) for angle in angles]

    edges = []
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            edges.append((i, j))

    return positions, edges


def percolate(edges, p, seed=None):
    rng = np.random.default_rng(seed)
    selected_edges = [edge for edge in edges if rng.random() < p]
    return selected_edges


def components_BFS(num_vertices, selected_edges):
    # Adj
    adj_list = {i: [] for i in range(num_vertices)}
    for i, j in selected_edges:
        adj_list[i].append(j)
        adj_list[j].append(i)

    visited = [False] * num_vertices
    components = []

    for vertex in range(num_vertices):
        if not visited[vertex]:
            component = bfs(vertex, visited, adj_list)
            components.append(component)

    return components



def bfs(start, visited, adj_list):
    component = []
    queue = deque([start])
    visited[start] = True
    while queue:
        node = queue.popleft()
        component.append(node)
        for neighbor in adj_list[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)
    return component
    


def get_colored_bond_lines(positions, edges, selected_edges, components, component_colors):
    colored_lines = []

    for i, j in selected_edges:
        x1, y1 = positions[i]
        x2, y2 = positions[j]
        line = [(x1 * spacing, y1 * spacing), (x2 * spacing, y2 * spacing)]

        component = None
        for comp in components:
            if i in comp and j in comp:
                component = tuple(sorted(comp))
                break

        # get current color
        color = component_colors[component]
        colored_lines.append((line, color))

    return colored_lines


fig = plt.figure(figsize=(10, 8))
gs = gridspec.GridSpec(1, 2, width_ratios=[4, 1])

ax = fig.add_subplot(gs[0])
ax.set_aspect('equal')
ax.set_xlim(-spacing, spacing)
ax.set_ylim(-spacing, spacing)
ax.axis('off')

control_ax = fig.add_subplot(gs[1])
control_ax.axis('off')

title = ax.set_title(f"Bond Percolation (n = {num_vertices}, p = {initial_p:.2f}, seed = {seed})", color='black', fontsize=16, ha="center")

# Init
positions, edges = generate_Kn(num_vertices)
selected_edges = percolate(edges, initial_p, seed)
components = components_BFS(num_vertices, selected_edges)
component_colors = {tuple(sorted(component)): (random.random(), random.random(), random.random()) for component in components}

# Use correct colors
colored_lines = get_colored_bond_lines(positions, edges, selected_edges, components, component_colors)
lines = [line for line, color in colored_lines]
colors = [color for line, color in colored_lines]
lc_all = LineCollection(lines, colors=colors, linewidths=1)
ax.add_collection(lc_all)

# Plot vertex by color
for i, position in enumerate(positions):
    vertex_color = None
    for comp in components:
        if i in comp:
            vertex_color = component_colors[tuple(sorted(comp))]
            break
    ax.plot(position[0] * spacing, position[1] * spacing, 'o', markersize=8, color=vertex_color)


# Sidebar
slider_ax = fig.add_axes([0.83, 0.45, 0.03, 0.4])
slider = Slider(slider_ax, 'p', 0.0, 0.15, valinit=initial_p, orientation='vertical')
button_ax = fig.add_axes([0.78, 0.2, 0.15, 0.05])
seed_button = Button(button_ax, 'New Seed')


def update(val):
    global seed

    p = slider.val
    selected_edges = percolate(edges, p, seed)
    components = components_BFS(num_vertices, selected_edges)

    # Merge & update if connected
    new_component_colors = {}
    for component in components:
        component_tuple = tuple(sorted(component))
        if component_tuple not in component_colors:
            component_colors[component_tuple] = (random.random(), random.random(), random.random())
        new_component_colors[component_tuple] = component_colors[component_tuple]


    colored_lines = get_colored_bond_lines(positions, edges, selected_edges, components, new_component_colors)
    lc_all.set_segments([line for line, color in colored_lines])
    lc_all.set_colors([color for line, color in colored_lines])

    # Update colors
    for i, position in enumerate(positions):
        vertex_color = None
        for comp in components:
            if i in comp:
                vertex_color = new_component_colors[tuple(sorted(comp))]
                break
        ax.plot(position[0] * spacing, position[1] * spacing, 'o', markersize=8, color=vertex_color)

    title.set_text(f"Bond Percolation (n = {num_vertices}, p = {p:.2f}, seed = {seed})")
    fig.canvas.draw_idle()


def change_seed(event):
    global seed
    seed += 1
    update(None)

slider.on_changed(update)
seed_button.on_clicked(change_seed)

plt.show()
