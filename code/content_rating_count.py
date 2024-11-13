import sqlite3
import pandas as pd

# Tengjast gagnagrunninum
db_path = "data/rotten_tomatoes.db"
conn = sqlite3.connect(db_path)

# Lesa leo_movies og kate_movies úr gagnagrunninum
leo_movies = pd.read_sql_query("SELECT content_rating FROM leo_movies", conn)
kate_movies = pd.read_sql_query("SELECT content_rating FROM kate_movies", conn)

# Vinna úr gögnum fyrir Leonardo DiCaprio
leo_movies_count = leo_movies \
    .groupby("content_rating") \
    .size() \
    .reset_index(name="count") \
    .assign(actor="Leonardo DiCaprio")
leo_movies_count["percentage"] = (leo_movies_count["count"] / leo_movies_count["count"].sum()) * 100

# Vinna úr gögnum fyrir Kate Winslet
kate_movies_count = kate_movies \
    .groupby("content_rating") \
    .size() \
    .reset_index(name="count") \
    .assign(actor="Kate Winslet")
kate_movies_count["percentage"] = (kate_movies_count["count"] / kate_movies_count["count"].sum()) * 100

# Sameina gögnin í eitt DataFrame
content_rating_count = pd.concat([leo_movies_count, kate_movies_count], ignore_index=True)

# Búa til nýja töflu í gagnagrunninum fyrir content_rating_count ef hún er ekki þegar til
with conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS content_rating_count (
            content_rating TEXT,
            count INTEGER,
            percentage REAL,
            actor TEXT
        )
    ''')
    # Hreinsa eldri gögn ef þau eru til
    conn.execute("DELETE FROM content_rating_count")

# Setja gögnin úr combined_movies_count í SQLite töfluna
content_rating_count.to_sql('content_rating_count', conn, if_exists='append', index=False)

# Loka tengingu við gagnagrunninn
conn.close()