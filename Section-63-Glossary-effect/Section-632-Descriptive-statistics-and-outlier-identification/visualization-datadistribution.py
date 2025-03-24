import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load your data
data_file = "output-system.csv"
data = pd.read_csv(data_file, delimiter="\t")

# Create histogram
plt.figure(figsize=(10, 6))
bins = 50  # Number of bins
hist, bin_edges = np.histogram(data['Frequency'], bins=bins)  # Get histogram data
plt.hist(data['Frequency'], bins=bins, color='blue', alpha=0.7, log=True, edgecolor='black')

# Add labels to each bar
for i in range(len(hist)):
    x = (bin_edges[i] + bin_edges[i + 1]) / 2  # Bin center
    y = hist[i]
    if y > 0:  # Only label non-zero bars
        plt.text(x, y, str(y), ha='center', va='bottom', fontsize=8, rotation=45)

# Add title and labels
plt.title("Frequency Distribution (Log Scale with Tags)")
plt.xlabel("Frequency")
plt.ylabel("Count (Log Scale)")

# Save the plot
plt.savefig("frequency_distribution_with_tags.png")
print("Plot saved as 'frequency_distribution_with_tags.png'")
