import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from tqdm import tqdm
import pandas as pd

def estimate_complete(n, p_values, num_trials):
    largest_components = []

    for p in tqdm(p_values):
        trial_largest = []
        for seed in range(num_trials):
            G = nx.erdos_renyi_graph(n, p, seed=seed)
            if len(G) == 0:
                trial_largest.append(0)
            else:
                largest_cc = max(nx.connected_components(G), key=len)
                trial_largest.append(len(largest_cc) / n)  # Norm
        largest_components.append(np.mean(trial_largest))

    return largest_components



n = 150
p_values = np.linspace(0, 0.15, 1000)
num_trials = 100

largest_components = estimate_complete(n, p_values, num_trials)
plt.figure(figsize=(8, 5))
plt.plot(p_values, largest_components, linestyle='-', color='darkgreen', label=f"n = {n}")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


df = pd.DataFrame({
    "p": p_values,
    "largest_components": largest_components
})
df.to_csv(f"cg_{n}_data.csv", index=False)
