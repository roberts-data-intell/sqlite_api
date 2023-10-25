import pandas as pd
from sqlalchemy import create_engine

try:
    # 1. Read Excel File
    print("Reading Excel file...")
    excel_data = pd.read_excel('sales.xlsx')
    print("Excel file has been read successfully.")

    # 2. Data Preprocessing (optional)
    print("Performing data preprocessing...")
    excel_data.dropna(inplace=True)
    print("Data preprocessing completed.")
  
    # 3. Connect to Database
    print("Connecting to database...")
    engine = create_engine('sqlite:///Sales_Project.db')
    print("Connected to database.")
  
    # 4. Load data into Database
    print("Loading data into database...")
    excel_data.to_sql('Business_Data', engine, index=False, if_exists='replace')
    print("Data has been loaded successfully!")
  
except FileNotFoundError:
    print("Error: The specified Excel file was not found.")
except pd.errors.EmptyDataError:
    print("Error: The Excel file is empty.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

