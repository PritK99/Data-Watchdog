import os
import pandas as pd

assets_folder = '../assets/data'
files = os.listdir(assets_folder)

# For all files in folder
for file_name in files:
    file_path = os.path.join(assets_folder, file_name)
    
    # We select only the CSV files
    if file_name.endswith('.csv'):
        df = pd.read_csv(file_path)
        
        # Printing metadata for CSV file
        print(f"File Name: {file_name}")
        print(f"Columns: {list(df.columns)}")
        print("Head:")
        print(df.head())
        print("\n" + "="*40 + "\n")

        # Additional work for analysing each column