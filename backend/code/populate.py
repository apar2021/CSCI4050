import pandas as pd
import os
import sqlite3 as sql
path = "C:/Users/cownj/OneDrive/Desktop/4050/CSCI4050Project/backend/code"
db_path = "C:/Users/cownj/OneDrive/Desktop/4050/CSCI4050Project/backend/code/instance/database.db"

# Print Current working directory
#print(os.getcwd())

# Swap to path directory
os.chdir(path)

df = pd.read_csv('dataset/books.csv').iloc[::40]
print(len(df))

#for row in [df]:
##    print(row['title'].values[0]) # Testing

print(df.columns)

with sql.connect(db_path) as con:
    # Create a cursor object
    cur = con.cursor()
    # Iterate through each row of the dataframe
    for _, row in df.iterrows():
        # Prepare data for SQL query
        data = (row['isbn10'], row['title'], row['authors'], row['edition'], row['categories'],
                row['publisher'], row['published_year'], row['thumbnail'], row['quantity'], 
                row['status'], row['selling_price'], row['buying_price'], row['min_threshold'])

        # Execute the SQL query
        cur.execute("""
                    INSERT INTO books 
                    (isbn, title, author, edition, category, publisher, publication_year, image_url,
                    quantity, status, selling_price, buying_price, min_threshold) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, data)

    # Commit the changes to the database
    con.commit()


# # Insert each row of the dataframe into the database located at db_path
# with sql.connect(db_path) as con:
#     # Iterate through each row of the dataframe
#     for row in [df]:
#         # Create a cursor object
#         cur = con.cursor()
#         # Execute the SQL query
#         cur.execute(f"""
#                     INSERT INTO books ({row['isbn10'].values[0]}, {row['title'].values[0]}, {row['authors'].values[0]}, {row['edition'].values[0]}, {row['categories'].values[0]},
#                     {row['publisher'].values[0]}, {row['published_year'].values[0]}, {row['thumbnail'].values[0]}, {row['quantity'].values[0]}, {row['status'].values[0]},
#                     {row['selling_price'].values[0]}, {row['buying_price'].values[0]}, {row['min_threshold'].values[0]}
#         """)
#         # Commit the changes to the database
#         con.commit()



