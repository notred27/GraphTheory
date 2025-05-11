import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random
import pandas as pd
from tqdm import tqdm


def generate_square(n):
    G = nx.grid_2d_graph(n, n)
    return G

def percolate(G, p):
    H = nx.Graph()
    H.add_nodes_from(G.nodes)
    for edge in G.edges:
        if random.random() < p:
            H.add_edge(*edge)
    return H

def cluster_from_origin(G, origin):
    if origin not in G:
        return 0
    try:
        cluster = nx.node_connected_component(G, origin)
        return len(cluster)
    except:
        return 0

def simulate(n, p_values, num_trials):
    mean_cluster_sizes = []
    base_graph = generate_square(n)
    origin = (n//2, n//2)

    for p in tqdm(p_values):
        sizes = []
        for _ in range(num_trials):
            H = percolate(base_graph, p)
            size = cluster_from_origin(H, origin)
            sizes.append(size)
        mean_cluster_sizes.append(np.mean(sizes))
    
    return mean_cluster_sizes


lattice_size = 200
num_trials = 30
p_values = np.linspace(0.1, 0.9, 30)

mean_sizes = simulate(lattice_size, p_values, num_trials)

plt.figure(figsize=(8, 5))
plt.plot(p_values, mean_sizes, color='blue')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

df = pd.DataFrame({
    "p": p_values,
    "mean_cluster_size": mean_sizes
})
df.to_csv("square_lattice_data.csv", index=False)

