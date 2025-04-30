import pandas as pd

# Load the CSV file with flexible handling of inconsistent columns
df = pd.read_csv("data/chunk_metadata.csv", header=0, dtype=str, on_bad_lines='skip')

# Display the first few rows to inspect the data
print(df.head())

# Fill missing values with a placeholder (e.g., 'N/A')
df.fillna('N/A', inplace=True)

# Rename columns if necessary
df.rename(columns=lambda x: x.strip(), inplace=True)

# Save the cleaned DataFrame to a new CSV file
df.to_csv("data/cleaned_chunk_metadata.csv", index=False)

