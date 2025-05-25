import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from tqdm import tqdm
import pandas as pd



def generate_triangle(L, p, rng):
    bonds = []
    for i in range(L):
        for j in range(L):
            neighbors = []
            if j + 1 < L:
                neighbors.append(((i, j), (i, j + 1)))
            if i + 1 < L:
                neighbors.append(((i, j), (i + 1, j)))
            if i + 1 < L and j - 1 >= 0 and i % 2 == 1:
                neighbors.append(((i, j), (i + 1, j - 1)))
            if i + 1 < L and j + 1 < L and i % 2 == 0:
                neighbors.append(((i, j), (i + 1, j + 1)))
            for (a, b) in neighbors:
                if rng.random() < p:
                    bonds.append((a, b))
    return bonds

def build_adjacency(L, bonds):
    graph = { (i, j): [] for i in range(L) for j in range(L) }
    for (node1, node2) in bonds:
        graph[node1].append(node2)
        graph[node2].append(node1)
    return graph

def cluster_size_from_center(L, graph):
    center = (L // 2, L // 2)
    visited = set()
    queue = deque([center])
    visited.add(center)
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return len(visited)

def simulate():
    results = []
    rng = np.random.default_rng(42)
    for p in tqdm(p_values):
        sizes = []
        for _ in range(num_trials):
            bonds = generate_triangle(L, p, rng)
            graph = build_adjacency(L, bonds)
            size = cluster_size_from_center(L, graph)
            sizes.append(size)
        mean_size = np.mean(sizes)
        results.append(mean_size)
    return results

L = 200
num_trials = 30
p_values = np.linspace(0.1, 1.0, 30)

mean_sizes = simulate()
plt.figure(figsize=(8, 5))
plt.plot(p_values, mean_sizes, color='blue')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

df = pd.DataFrame({
    "p": p_values,
    "mean_cluster_size": mean_sizes
})
df.to_csv("triangle_lattice_data.csv", index=False)
