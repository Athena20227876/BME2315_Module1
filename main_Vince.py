import pandas as pd

df = pd.read_csv('Metadata and Protein Data for Module 1.csv')

for header in df.columns:
    print(header)
