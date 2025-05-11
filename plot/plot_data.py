
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

plt.figure(figsize=(8, 5))

df = pd.read_csv("cube_lattice_data.csv")
p_values = df["p"].values
mean_sizes = df["mean_cluster_size"].values
plt.plot(p_values, mean_sizes, color='blue', label="Cube Lattice")
plt.axvline(0.2488, linestyle='--', color='darkblue', label=r"$p_c \approx 0.2488$")



df = pd.read_csv("square_lattice_data.csv")
p_values = df["p"].values
mean_sizes = df["mean_cluster_size"].values
plt.plot(p_values, mean_sizes,color='orange', label="Square Lattice")
plt.axvline(0.5, linestyle='--', color='darkorange', label=r"$p_c = 0.5$")


df = pd.read_csv("triangle_lattice_data.csv")
p_values = df["p"].values
mean_sizes = df["mean_cluster_size"].values
plt.plot(p_values, mean_sizes,  color='red', label="Triangle Lattice")
plt.axvline(np.sin(np.pi/ 18) * 2, linestyle='--', color='darkred', label=r"$p_c = 2\sin(\frac{pi}{18})$")

plt.title("Mean Cluster Containing Origin vs p")
plt.xlabel("Bond Probability p")
plt.ylabel("Mean Cluster Containing Origin")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


