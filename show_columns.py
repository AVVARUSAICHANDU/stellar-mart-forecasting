import pandas as pd

# change the filename only if your Excel file has a different name
path = "data/StellarMart_Raw_Dataset_final.xlsx"

try:
    df = pd.read_excel(path, nrows=2)
    print("SUCCESS: Read file at", path)
    print("Columns (exact):")
    print(df.columns.tolist())
except FileNotFoundError:
    print("ERROR: File not found. Make sure the Excel file is at:", path)
except Exception as e:
    print("ERROR:", str(e))
