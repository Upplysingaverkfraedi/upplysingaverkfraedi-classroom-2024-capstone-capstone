import sqlite3
import re


db_path = "data/rotten_tomatoes.db"

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# SQL query to create a new table 'leo_movies' with movies where Leonardo DiCaprio is an actor
# This query first checks if 'leo_movies' table exists and deletes it to avoid duplication
cursor.execute("DROP TABLE IF EXISTS leo_movies")
cursor.execute("""
    CREATE TABLE leo_movies AS
    SELECT *
    FROM rotten_tomatoes_movies_dicaprio_winslet
    WHERE actors LIKE '%Leonardo DiCaprio%'
""")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Taflan 'leo_movies' hefur verið gert!")