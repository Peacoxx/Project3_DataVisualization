import pandas as pd
import sqlite3

# Load the csv FastFoodNutritionMenuV2 from the resources folder. 
csv_path = ('../resources/FastFoodNutritionMenuV2.csv')
fastfooddata = pd.read_csv(csv_path)

# display the first 5 rows of the data
fastfooddata.head()

# Connect to your database
conn = sqlite3.connect('fastfood.db')

# Check existing tables
tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
print(tables)

# Attempt to read from the 'menu' table
# try:
#     df = pd.read_sql_query("SELECT * FROM menu", conn)
#     print(df)
# except pd.io.sql.DatabaseError as e:
#     print("An error occurred:", e)