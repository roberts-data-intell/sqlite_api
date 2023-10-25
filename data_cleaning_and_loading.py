import pandas as pd
from sqlalchemy import create_engine

# Read Excel File
excel_data = pd.read_excel('sales.xlsx')

# Data Preprocessing

## Type Validation
integer_columns = ['Area Code', 'ProductId']
float_columns = ['Market Size', 'Profit', 'Margin', 'Sales', 'COGS', 'Total Expenses', 'Marketing', 'Inventory', 'Budget Profit', 'Budget COGS', 'Budget Sales']

for col in integer_columns:
    excel_data[col] = excel_data[col].astype(int, errors='ignore')

for col in float_columns:
    excel_data[col] = excel_data[col].astype(float, errors='ignore')

## Missing Values
# Replace NaN with 0 for numerical columns
excel_data[float_columns + integer_columns] = excel_data[float_columns + integer_columns].fillna(0)

# Replace NaN with 'Unknown' for string columns
string_columns = ['State', 'Market', 'Product Type', 'Product', 'Type']
excel_data[string_columns] = excel_data[string_columns].fillna('Unknown')

## Date Formatting
excel_data['Date'] = pd.to_datetime(excel_data['Date'], errors='coerce')

## Text Cleaning
excel_data['State'] = excel_data['State'].str.upper()
excel_data['Market'] = excel_data['Market'].str.upper()
excel_data['Product Type'] = excel_data['Product Type'].str.upper()
excel_data['Product'] = excel_data['Product'].str.upper()
excel_data['Type'] = excel_data['Type'].str.upper()

## Range Checks
# Remove rows where Profit, Margin, or any other financial metric is negative
financial_metrics = ['Profit', 'Margin', 'Sales', 'COGS', 'Total Expenses', 'Marketing', 'Inventory', 'Budget Profit', 'Budget COGS', 'Budget Sales']
excel_data = excel_data[(excel_data[financial_metrics] >= 0).all(axis=1)]

## Duplicate Rows
excel_data.drop_duplicates(inplace=True)

# Connect to Database
engine = create_engine('sqlite:///Sales_Project.db')

# Load cleaned data into Database
excel_data.to_sql('Business_Data', engine, index=False, if_exists='replace')

print("Data has been cleaned and loaded successfully!")