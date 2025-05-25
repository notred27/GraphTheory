
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

plt.figure(figsize=(8, 5))

df = pd.read_csv("cg_50_data.csv")
p_values = df["p"].values
mean_sizes = df["largest_components"].values
plt.plot(p_values, mean_sizes, color='blue', label=r"$K_{50}$")
plt.axvline(0.02, linestyle='--', color='darkblue', label=r"$p_c \approx 0.02$")



df = pd.read_csv("cg_100_data.csv")
p_values = df["p"].values
mean_sizes = df["largest_components"].values
plt.plot(p_values, mean_sizes,color='orange', label=r"$K_{100}$")
plt.axvline(0.01, linestyle='--', color='darkorange', label=r"$p_c \approx 0.01$")


df = pd.read_csv("cg_150_data.csv")
p_values = df["p"].values
mean_sizes = df["largest_components"].values
plt.plot(p_values, mean_sizes,  color='red', label=r"$K_{150}$")
plt.axvline(0.0066, linestyle='--', color='darkred', label=r"$p_c \approx 0.00667$")

plt.title("Largest Connected Component vs p")
plt.xlabel("Bond Probability p")
plt.ylabel("Size of Largest Connected Component")
plt.xlim(0, 0.1)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


