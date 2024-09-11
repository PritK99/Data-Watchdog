import os
import pandas as pd
from sqlalchemy import create_engine, inspect

# PostgreSQL database credentials
db_host = "dpg-crg0vsrv2p9s73a55u70-a.oregon-postgres.render.com"
db_user = "data_jvjt_user"
db_password = "az4dtMhSZlWHXhrKtIangaf1nFulxMba"
db_name = "data_jvjt"
db_port = 5432

# Relative path where CSV files should be saved (relative to the script's location)
relative_csv_directory = '\output'  # Replace with your desired relative path
print(os.getcwd())
# Convert relative path to an absolute path
csv_directory = os.getcwd()+relative_csv_directory

# Ensure the directory exists, if not, create it
if not os.path.exists(csv_directory):
    os.makedirs(csv_directory)
    print(f"Directory {csv_directory} created.")

# Create a connection string and engine
engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# Create an inspector object to get table names
inspector = inspect(engine)

# Get all table names
table_names = inspector.get_table_names()

# Loop through all tables and save them as CSV
for table_name in table_names:
    # Load table into a pandas DataFrame
    query = f'SELECT * FROM {table_name}'
    df = pd.read_sql(query, engine)
    
    # Create the CSV file path
    csv_file_path = os.path.join(csv_directory, f'{table_name}.csv')
    
    # Check if the CSV file already exists
    if os.path.exists(csv_file_path):
        print(f"CSV file for table {table_name} already exists at {csv_file_path}. Skipping...")
    else:
        # Save DataFrame to CSV with the table name as the file name
        df.to_csv(csv_file_path, index=False)
        print(f"Table {table_name} has been written to {csv_file_path}")

# Close the database connection
engine.dispose()
