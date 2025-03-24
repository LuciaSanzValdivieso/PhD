import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# Load your combined CSV file
data_file = "output.csv"  # Replace with your CSV file name
data = pd.read_csv(data_file, delimiter="\t")  # Assuming tab-delimited CSV

# Descriptive statistics
stats = data.groupby('Translation Accuracy')['Frequency'].describe()
print("Descriptive Statistics:\n", stats)

# Visualization
plt.figure(figsize=(10, 6))
data.boxplot(column='Frequency', by='Translation Accuracy', grid=False)
plt.title('Frequency vs. Translation Accuracy')
plt.suptitle('')  # Remove default title
plt.ylabel('Frequency')
plt.xlabel('Translation Accuracy')
plt.show()

# Statistical test
correct_freq = data[data['Translation Accuracy'] == 'Correct']['Frequency']
incorrect_freq = data[data['Translation Accuracy'] == 'Incorrect']['Frequency']
t_stat, p_value = ttest_ind(correct_freq, incorrect_freq, equal_var=False)  # Welch's t-test
print(f"T-test results: t-statistic = {t_stat}, p-value = {p_value}")
