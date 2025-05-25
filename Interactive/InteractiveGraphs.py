import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons, Button
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from matplotlib.collections import LineCollection
from collections import deque

# Setup for dim
L_2d = 50
L_3d = 10
initial_p = 0.3
seed = 0
BFS_left = True 


def generate_bond_square(L, p, seed=None):
    rng = np.random.default_rng(seed)
    h_bonds = rng.random((L, L - 1)) < p
    v_bonds = rng.random((L - 1, L)) < p
    return h_bonds, v_bonds

def build_square_adjacency(L, h_bonds, v_bonds):
    graph = {(i, j): [] for i in range(L) for j in range(L)}
    for i in range(L):
        for j in range(L - 1):
            if h_bonds[i, j]:
                graph[(i, j)].append((i, j + 1))
                graph[(i, j + 1)].append((i, j))
    for i in range(L - 1):
        for j in range(L):
            if v_bonds[i, j]:
                graph[(i, j)].append((i + 1, j))
                graph[(i + 1, j)].append((i, j))
    return graph

def bfs_2d(L, graph, from_left=True):
    visited = set()
    queue = deque()
    if from_left:
        for i in range(L):
            start = (i, 0)
            queue.append(start)
            visited.add(start)
    else:
        start = (L // 2, L // 2)
        queue.append(start)
        visited.add(start)
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return visited

def get_colored_lines_square(L, h_bonds, v_bonds, component):
    blue_lines, red_lines = [], []
    for i in range(L):
        for j in range(L - 1):
            a, b = (i, j), (i, j + 1)
            line = [(j, L - 1 - i), (j + 1, L - 1 - i)]
            if h_bonds[i, j]:
                (red_lines if a in component and b in component else blue_lines).append(line)
    for i in range(L - 1):
        for j in range(L):
            a, b = (i, j), (i + 1, j)
            line = [(j, L - 1 - i), (j, L - 2 - i)]
            if v_bonds[i, j]:
                (red_lines if a in component and b in component else blue_lines).append(line)
    return blue_lines, red_lines

def generate_bond_cube(L, p, seed=None):
    rng = np.random.default_rng(seed)
    x_bonds = rng.random((L, L, L - 1)) < p
    y_bonds = rng.random((L, L - 1, L)) < p
    z_bonds = rng.random((L - 1, L, L)) < p
    return x_bonds, y_bonds, z_bonds

def build_adjacency_cube(L, x_bonds, y_bonds, z_bonds):
    graph = {(i, j, k): [] for i in range(L) for j in range(L) for k in range(L)}
    for i in range(L):
        for j in range(L):
            for k in range(L - 1):
                if x_bonds[i, j, k]:
                    graph[(i, j, k)].append((i, j, k + 1))
                    graph[(i, j, k + 1)].append((i, j, k))
    for i in range(L):
        for j in range(L - 1):
            for k in range(L):
                if y_bonds[i, j, k]:
                    graph[(i, j, k)].append((i, j + 1, k))
                    graph[(i, j + 1, k)].append((i, j, k))
    for i in range(L - 1):
        for j in range(L):
            for k in range(L):
                if z_bonds[i, j, k]:
                    graph[(i, j, k)].append((i + 1, j, k))
                    graph[(i + 1, j, k)].append((i, j, k))
    return graph


def bfs_3d(L, graph, from_face=True):
    visited = set()
    queue = deque()
    if from_face:
        for i in range(L):
            for j in range(L):
                start = (i, j, 0)
                queue.append(start)
                visited.add(start)
    else:
        start = (L//2, L//2, L//2)
        queue.append(start)
        visited.add(start)
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return visited

def get_colored_lines_cube(L, x_bonds, y_bonds, z_bonds, component):
    blue_lines, red_lines = [], []
    for i in range(L):
        for j in range(L):
            for k in range(L - 1):
                a, b = (i, j, k), (i, j, k + 1)
                if x_bonds[i, j, k]:
                    line = [(k, j, i), (k + 1, j, i)]
                    (red_lines if a in component and b in component else blue_lines).append(line)
    for i in range(L):
        for j in range(L - 1):
            for k in range(L):
                a, b = (i, j, k), (i, j + 1, k)
                if y_bonds[i, j, k]:
                    line = [(k, j, i), (k, j + 1, i)]
                    (red_lines if a in component and b in component else blue_lines).append(line)
    for i in range(L - 1):
        for j in range(L):
            for k in range(L):
                a, b = (i, j, k), (i + 1, j, k)
                if z_bonds[i, j, k]:
                    line = [(k, j, i), (k, j, i + 1)]
                    (red_lines if a in component and b in component else blue_lines).append(line)
    return blue_lines, red_lines




def generate_bond_triangular(L, p, seed=None):
    rng = np.random.default_rng(seed)
    bonds = []
    for i in range(L):
        for j in range(L):
            neighbors = []
            if j + 1 < L:
                neighbors.append(((i, j), (i, j + 1)))
            if i + 1 < L:
                neighbors.append(((i, j), (i + 1, j)))
            if i + 1 < L and j + 1 < L and i % 2 == 1:
                neighbors.append(((i, j), (i + 1, j + 1)))
            if i + 1 < L and j - 1 >= 0 and i % 2 == 0:
                neighbors.append(((i, j), (i + 1, j - 1)))
            for a, b in neighbors:
                if rng.random() < p:
                    bonds.append((a, b))
    return bonds

def build_adjacency_triangular(L, bonds):
    graph = {(i, j): [] for i in range(L) for j in range(L)}
    for a, b in bonds:
        graph[a].append(b)
        graph[b].append(a)
    return graph



def get_colored_lines_triangular(L, bonds, component):
    blue_lines = []
    red_lines = []
    for (a, b) in bonds:
        y1, x1 = a
        y2, x2 = b
        dx = 0.5 if y1 % 2 == 1 else 0
        dx2 = 0.5 if y2 % 2 == 1 else 0
        pt1 = (x1 + dx, L - 1 - y1)
        pt2 = (x2 + dx2, L - 1 - y2)
        if a in component and b in component:
            red_lines.append([pt1, pt2])
        else:
            blue_lines.append([pt1, pt2])
    return blue_lines, red_lines




fig = plt.figure(figsize=(10, 8))
ax2d = fig.add_subplot(111)
ax3d = fig.add_subplot(111, projection='3d')
ax3d.set_box_aspect([1,1,1])


# Create sidebar
slider_ax = fig.add_axes([0.83, 0.7, 0.12, 0.03])
slider = Slider(slider_ax, 'p', 0, 1, valinit=initial_p)

view_radio_ax = fig.add_axes([0.83, 0.55, 0.12, 0.1])
view_radio = RadioButtons(view_radio_ax, ['Square', 'Triangular', 'Cube'], 0)

start_radio_ax = fig.add_axes([0.83, 0.4, 0.12, 0.1])
start_radio = RadioButtons(start_radio_ax, ['From Left/Face', 'From Center'], 0)

button_ax = fig.add_axes([0.83, 0.3, 0.12, 0.05])
seed_button = Button(button_ax, 'New Seed')


def draw_all():
    global lc2d, hl2d, lc3d, hl3d

    p = slider.val
    ax2d.clear()
    ax3d.cla()


    if view_radio.value_selected == 'Square':
        h_bonds, v_bonds = generate_bond_square(L_2d, p, seed)
        g2d = build_square_adjacency(L_2d, h_bonds, v_bonds)
        comp2d = bfs_2d(L_2d, g2d, BFS_left)
        b2d, r2d = get_colored_lines_square(L_2d, h_bonds, v_bonds, comp2d)
        lc2d = LineCollection(b2d, colors='gray', linewidths=0.5)
        hl2d = LineCollection(r2d, colors='blue', linewidths=1.5)
        ax2d.add_collection(lc2d)
        ax2d.add_collection(hl2d)
        ax2d.set_xlim(-1, L_2d)
        ax2d.set_ylim(-1, L_2d)
        ax2d.set_aspect('equal')
        ax2d.axis('off')

    if view_radio.value_selected == 'Cube':
        x, y, z = generate_bond_cube(L_3d, p, seed)
        g3d = build_adjacency_cube(L_3d, x, y, z)
        comp3d = bfs_3d(L_3d, g3d, BFS_left)
        b3d, r3d = get_colored_lines_cube(L_3d, x, y, z, comp3d)
        lc3d = Line3DCollection(b3d, colors='gray', linewidths=0.5)
        hl3d = Line3DCollection(r3d, colors='blue', linewidths=1.5)
        ax3d.add_collection3d(lc3d)
        ax3d.add_collection3d(hl3d)
        ax3d.set_xlim(0, L_3d)
        ax3d.set_ylim(0, L_3d)
        ax3d.set_zlim(0, L_3d)
        ax3d.axis('off')


    if view_radio.value_selected == 'Triangular':
        ax2d.clear()
        bonds = generate_bond_triangular(L_2d, p, seed)
        gtri = build_adjacency_triangular(L_2d, bonds)
        comptri = bfs_2d(L_2d, gtri, BFS_left)
        btri, rtri = get_colored_lines_triangular(L_2d, bonds, comptri)

        # print(btri)
        lc_tri = LineCollection(btri, colors='gray', linewidths=0.5)
        hl_tri = LineCollection(rtri, colors='blue', linewidths=1.5)
        ax2d.add_collection(lc_tri)
        ax2d.add_collection(hl_tri)
        ax2d.set_xlim(-1, L_2d)
        ax2d.set_ylim(-1, L_2d)
        ax2d.set_aspect('equal')
        ax2d.axis('off')

    update_view()



def update_view(label=None):
    if view_radio.value_selected in ['Square', 'Triangular', 'Honeycomb']:
        ax2d.set_visible(True)
        ax3d.set_visible(False)
    else:
        ax2d.set_visible(False)
        ax3d.set_visible(True)
        
    fig.canvas.draw_idle()


def update_slider(val):
    draw_all()

def update_start_pos(label):
    global BFS_left
    BFS_left = (label == 'From Left/Face')
    draw_all()

def update_seed(event):
    global seed
    seed += 1
    draw_all()

slider.on_changed(update_slider)
view_radio.on_clicked(update_view)
view_radio.on_clicked(lambda _: draw_all())
start_radio.on_clicked(update_start_pos)
seed_button.on_clicked(update_seed)

draw_all()
plt.show()
