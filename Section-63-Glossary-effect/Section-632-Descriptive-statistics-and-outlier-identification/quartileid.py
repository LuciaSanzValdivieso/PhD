import pandas as pd

# Load your combined CSV file
data_file = "output-system.csv"  # Replace with your file name
data = pd.read_csv(data_file, delimiter="\t")  # Assuming tab-delimited file

# Calculate IQR
q1 = data['Frequency'].quantile(0.25)
q3 = data['Frequency'].quantile(0.75)
iqr = q3 - q1

# Define outlier bounds
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

# Filter out outliers
filtered_data = data[(data['Frequency'] >= lower_bound) & (data['Frequency'] <= upper_bound)]

# Save the filtered data
filtered_data.to_csv("filtered_data.csv", sep="\t", index=False)

# Print thresholds and summary
print(f"Lower Bound: {lower_bound}, Upper Bound: {upper_bound}")
print(filtered_data.describe())
