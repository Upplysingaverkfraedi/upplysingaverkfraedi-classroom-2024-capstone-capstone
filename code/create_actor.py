import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('data/rotten_tomatoes.db')
cursor = conn.cursor()

# Truncate (clear) the movie_actors table if it already exists
cursor.execute("DROP TABLE IF EXISTS movie_actors;")

# Create the movie_actors table with actor_id set to NULL for all entries
cursor.execute("""
    CREATE TABLE movie_actors (
        actor_id INTEGER NULL,
        movie_id INTEGER,
        actor_name TEXT,
        FOREIGN KEY (movie_id) REFERENCES rotten_tomatoes_movies_dicaprio_winslet(movie_id)
    );
""")

# Retrieve movie_id and actors columns from rotten_tomatoes_movies_dicaprio_winslet table
cursor.execute("SELECT movie_id, actors FROM rotten_tomatoes_movies_dicaprio_winslet")
rows = cursor.fetchall()

# Un-nest actors and insert into movie_actors table with actor_id set to NULL
for row in rows:
    movie_id, actors = row
    actor_list = [actor.strip() for actor in actors.split(',')]  # Split and strip whitespace
    for actor in actor_list:
        cursor.execute("INSERT INTO movie_actors (actor_id, movie_id, actor_name) VALUES (?, ?, ?)", (None, movie_id, actor))

# Commit the transaction and close the connection
conn.commit()
conn.close()
