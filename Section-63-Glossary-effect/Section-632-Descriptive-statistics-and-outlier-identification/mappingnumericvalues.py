import pandas as pd
import statsmodels.api as sm

# Step 1: Load the dataset
data = pd.read_csv('output-system.csv', sep='\t')  # Replace 'your_data.csv' with your file name

# Step 2: Map "Correct" and "Incorrect" to numeric values
data['Translation Accuracy'] = data['Translation Accuracy'].map({
    'Correct': 1,
    'Incorrect': 0
})

# Step 3: Handle unmapped or missing values
data = data.dropna(subset=['Translation Accuracy'])

# Step 4: Verify that both columns are numeric
print("Data types after mapping:")
print(data.dtypes)

# Optional: Print a sample of the cleaned data
print("\nSample of the cleaned data:")
print(data.head())

# Step 5: Save the updated data to a new file
data.to_csv('dataforregression-Marian.csv', index=False, sep='\t')  # Save the cleaned dataset
