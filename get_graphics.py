#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("hit_rates.csv")

df["size_kb"] = df["sets"].astype(int) * df["ways"].astype(int) * 64 // 1024

def get_policy(row):
    if row["replacement"] == "lru":
        return "LRU"
    elif row["replacement"] == "ship" and row["prefetcher"] == "no":
        return "SHIP (no prefetch)"
    else:
        return "SHIP + SPP"

df["policy"] = df.apply(get_policy, axis=1)

def geom_mean(x):
    return np.exp(np.mean(np.log(x)))

grouped = df.groupby(["policy", "size_kb"])["hit_rate"].agg(geom_mean).reset_index()
grouped = grouped.sort_values("size_kb")

plt.figure(figsize=(10, 6))
for policy in grouped["policy"].unique():
    data = grouped[grouped["policy"] == policy]
    plt.plot(data["size_kb"], data["hit_rate"], marker='o', linewidth=2, label=policy)

plt.xlabel("L2 Cache Size (KB)", fontsize=12)
plt.ylabel("Geometric Mean Hit Rate", fontsize=12)
plt.title("L2 Cache Hit Rate vs Size for Different Policies", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig("hit_rate_plot.png", dpi=150)
plt.show()
