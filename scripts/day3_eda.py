import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/raw/07_scheme_performance.csv")

rating = df["morningstar_rating"].value_counts().sort_index()

plt.figure(figsize=(8,6))

rating.plot(kind="bar")

plt.title("Morningstar Rating Distribution")

plt.tight_layout()

plt.savefig("reports/charts/morningstar_distribution.png")

print("Morningstar Rating Chart Saved")
