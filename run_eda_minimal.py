import pandas as pd

path = "data/StellarMart_Raw_Dataset_final.xlsx"
df = pd.read_excel(path)

col_map = {
    'Transaction ID': 'transaction_id',
    'Date of Sale': 'transaction_date',
    'Product Name': 'product_id',
    'Category': 'category',
    'Region': 'region',
    'Quantity Sold': 'quantity',
    'Sale Price': 'unit_price',
    'Total Sales': 'sales_amount'
}

df = df.rename(columns=col_map)
df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')

df = df.dropna(subset=['transaction_id','transaction_date','product_id','sales_amount'])

daily = df.groupby(pd.Grouper(key='transaction_date', freq='D'))['sales_amount'].sum().reset_index()
daily = daily.rename(columns={'sales_amount':'daily_sales'})

daily.to_csv("data/daily_sales.csv", index=False)

print("Saved → data/daily_sales.csv")
print("Preview:")
print(daily.head())
