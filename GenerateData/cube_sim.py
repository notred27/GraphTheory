import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from tqdm import tqdm
import pandas as pd

def generate_cube(L, p, seed=None):
    rng = np.random.default_rng(seed)
    x_bonds = rng.random((L, L, L - 1)) < p
    y_bonds = rng.random((L, L - 1, L)) < p
    z_bonds = rng.random((L - 1, L, L)) < p
    return x_bonds, y_bonds, z_bonds

def build_adjacency(L, x_bonds, y_bonds, z_bonds):
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

def cluster_size_from_center(L, graph):
    center = (L // 2, L // 2, L // 2)
    visited = set([center])
    queue = deque([center])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return len(visited)

def simulate(L, p_values, num_trials):
    mean_sizes = []
    for p in tqdm(p_values):
        sizes = []
        for trial in range(num_trials):
            x_bonds, y_bonds, z_bonds = generate_cube(L, p, seed=trial)
            graph = build_adjacency(L, x_bonds, y_bonds, z_bonds)
            sizes.append(cluster_size_from_center(L, graph))
        mean_sizes.append(np.mean(sizes))
    return mean_sizes


L = 35
p_values = np.linspace(0.1, 0.4, 30)
num_trials = 30


mean_sizes = simulate(L, p_values, num_trials)
plt.figure(figsize=(8, 5))
plt.plot(p_values, mean_sizes, color='blue', label="Cube")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

df = pd.DataFrame({
    "p": p_values,
    "mean_cluster_size": mean_sizes
})
df.to_csv("cube_lattice_data.csv", index=False)