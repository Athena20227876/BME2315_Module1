import pandas as pd
df = pd.read_csv("C:/Users/makay/OneDrive - University of Virginia/BME 2315/Module 1/Metadata and Protein Data for Module 1.csv")

for header in df.columns:
    print(header)