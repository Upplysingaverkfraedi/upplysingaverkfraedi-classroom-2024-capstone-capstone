import sqlite3
import re

# Path to your SQLite database
db_path = "data/rotten_tomatoes.db"

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Step 1: Drop the `main_actors_in_info` table if it already exists
cursor.execute("DROP TABLE IF EXISTS main_actors_in_info")

# Step 2: Create the `main_actors_in_info` table with the same schema as `rotten_tomatoes_movies_dicaprio_winslet`,
# but with `actor_in_info` instead of `actors`
cursor.execute("""
    CREATE TABLE main_actors_in_info AS
    SELECT
        rotten_tomatoes_link,
        NULL AS actor_in_info,  -- New column for individual actor
        movie_title,
        movie_info,
        critics_consensus,
        content_rating,
        genres,
        directors,
        authors,
        original_release_date,
        streaming_release_date,
        runtime,
        production_company,
        tomatometer_status,
        tomatometer_rating,
        tomatometer_count,
        audience_status,
        audience_rating,
        audience_count,
        tomatometer_top_critics_count,
        tomatometer_fresh_critics_count,
        tomatometer_rotten_critics_count,
        movie_id,
        actors,
        processed  
    FROM rotten_tomatoes_movies_dicaprio_winslet WHERE 0
""")

# Step 3: Fetch data from `rotten_tomatoes_movies_dicaprio_winslet`
cursor.execute("SELECT * FROM rotten_tomatoes_movies_dicaprio_winslet")
columns = [description[0] for description in cursor.description]  # Get column names
movies_data = cursor.fetchall()

# Step 4: Insert rows into `main_actors_in_info` with each actor extracted
for row in movies_data:
    movie_dict = dict(zip(columns, row))  # Convert row to a dictionary for easy access
    movie_info = movie_dict["movie_info"]

    # Extract individual actors from `movie_info` using regex
    actors_in_parentheses = re.findall(r"\(([^)]+)\)", movie_info)
    if actors_in_parentheses:
        # If actors are found within parentheses in `movie_info`
        for actors_group in actors_in_parentheses:
            for actor in actors_group.split(","):
                cleaned_actor = actor.strip()
                if cleaned_actor:
                    # Update the actor_in_info field
                    movie_dict["actor_in_info"] = cleaned_actor
                    # Insert the row into the new table
                    insert_columns = columns + ['actor_in_info']
                    cursor.execute(f"""
                        INSERT INTO main_actors_in_info ({', '.join(insert_columns)})
                        VALUES ({', '.join(['?' for _ in insert_columns])})
                    """, tuple(movie_dict[col] if col != 'actor_in_info' else cleaned_actor for col in insert_columns))
    else:
        # If no actors found in `movie_info`, extract the first five actors from the `actors` column
        actors_list = movie_dict["actors"].split(",")  # Split the actors column by comma
        first_five_actors = [actor.strip() for actor in actors_list[:5]]  # Get first five actors
        for actor in first_five_actors:
            if actor:
                # Update the actor_in_info field
                movie_dict["actor_in_info"] = actor
                # Insert the row into the new table
                insert_columns = columns + ['actor_in_info']
                cursor.execute(f"""
                    INSERT INTO main_actors_in_info ({', '.join(insert_columns)})
                    VALUES ({', '.join(['?' for _ in insert_columns])})
                """, tuple(movie_dict[col] if col != 'actor_in_info' else actor for col in insert_columns))

# Step 5: Manually add specific actors as per the request

# Add Leonardo DiCaprio for Romeo + Juliet (movie_id=17399)
cursor.execute("""
    INSERT INTO main_actors_in_info (rotten_tomatoes_link, actor_in_info, movie_title, movie_info, 
        critics_consensus, content_rating, genres, directors, authors, original_release_date, 
        streaming_release_date, runtime, production_company, tomatometer_status, tomatometer_rating, 
        tomatometer_count, audience_status, audience_rating, audience_count, 
        tomatometer_top_critics_count, tomatometer_fresh_critics_count, tomatometer_rotten_critics_count, movie_id)
    SELECT 
        rotten_tomatoes_link, 'Leonardo DiCaprio', movie_title, movie_info, critics_consensus, content_rating,
        genres, directors, authors, original_release_date, streaming_release_date, runtime,
        production_company, tomatometer_status, tomatometer_rating, tomatometer_count, audience_status,
        audience_rating, audience_count, tomatometer_top_critics_count, tomatometer_fresh_critics_count,
        tomatometer_rotten_critics_count, movie_id
    FROM rotten_tomatoes_movies_dicaprio_winslet
    WHERE movie_id = 17399
""")

# Add Kate Winslet for Triple 9 (movie_id=16495)
cursor.execute("""
    INSERT INTO main_actors_in_info (rotten_tomatoes_link, actor_in_info, movie_title, movie_info, 
        critics_consensus, content_rating, genres, directors, authors, original_release_date, 
        streaming_release_date, runtime, production_company, tomatometer_status, tomatometer_rating, 
        tomatometer_count, audience_status, audience_rating, audience_count, 
        tomatometer_top_critics_count, tomatometer_fresh_critics_count, tomatometer_rotten_critics_count, movie_id)
    SELECT 
        rotten_tomatoes_link, 'Kate Winslet', movie_title, movie_info, critics_consensus, content_rating,
        genres, directors, authors, original_release_date, streaming_release_date, runtime,
        production_company, tomatometer_status, tomatometer_rating, tomatometer_count, audience_status,
        audience_rating, audience_count, tomatometer_top_critics_count, tomatometer_fresh_critics_count,
        tomatometer_rotten_critics_count, movie_id
    FROM rotten_tomatoes_movies_dicaprio_winslet
    WHERE movie_id = 16495
""")

# Add Kate Winslet for Christmas Carol: The Movie (movie_id=4571)
cursor.execute("""
    INSERT INTO main_actors_in_info (rotten_tomatoes_link, actor_in_info, movie_title, movie_info, 
        critics_consensus, content_rating, genres, directors, authors, original_release_date, 
        streaming_release_date, runtime, production_company, tomatometer_status, tomatometer_rating, 
        tomatometer_count, audience_status, audience_rating, audience_count, 
        tomatometer_top_critics_count, tomatometer_fresh_critics_count, tomatometer_rotten_critics_count, movie_id)
    SELECT 
        rotten_tomatoes_link, 'Kate Winslet', movie_title, movie_info, critics_consensus, content_rating,
        genres, directors, authors, original_release_date, streaming_release_date, runtime,
        production_company, tomatometer_status, tomatometer_rating, tomatometer_count, audience_status,
        audience_rating, audience_count, tomatometer_top_critics_count, tomatometer_fresh_critics_count,
        tomatometer_rotten_critics_count, movie_id
    FROM rotten_tomatoes_movies_dicaprio_winslet
    WHERE movie_id = 4571
""")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Table 'main_actors_in_info' has been created successfully with individual actors in 'actor_in_info' including manual additions.")