import sqlite3

# Tengjast gagnagrunninum
conn = sqlite3.connect('data/rotten_tomatoes.db')
cursor = conn.cursor()

# Keyra SQL-fyrirspurnir
queries = [
    """
    CREATE TABLE IF NOT EXISTS top10_tomatometer_movies AS
    SELECT 
        movie_title, 
        tomatometer_rating, 
        audience_rating, 
        directors, 
        actors, 
        original_release_date
    FROM 
        rotten_tomatoes_movies
    WHERE 
        actors LIKE '%Kate Winslet%' OR actors LIKE '%Leonardo DiCaprio%'
    ORDER BY 
        tomatometer_rating DESC
    LIMIT 10;
    """,
    """
    CREATE TABLE IF NOT EXISTS top10_audience_movies AS
    SELECT 
        movie_title, 
        tomatometer_rating, 
        audience_rating, 
        directors, 
        actors, 
        original_release_date
    FROM 
        rotten_tomatoes_movies
    WHERE 
        actors LIKE '%Kate Winslet%' OR actors LIKE '%Leonardo DiCaprio%'
    ORDER BY 
        audience_rating DESC
    LIMIT 10;
    """,
    """
    CREATE TABLE IF NOT EXISTS all_movies_tomatometer_directors AS
    SELECT 
        movie_title, 
        tomatometer_rating, 
        audience_rating, 
        directors, 
        actors, 
        original_release_date
    FROM 
        rotten_tomatoes_movies
    WHERE 
        directors IN (
            SELECT DISTINCT directors 
            FROM top10_tomatometer_movies
        );
    """,
    """
    CREATE TABLE IF NOT EXISTS all_movies_audience_directors AS
    SELECT 
        movie_title, 
        tomatometer_rating, 
        audience_rating, 
        directors, 
        actors, 
        original_release_date
    FROM 
        rotten_tomatoes_movies
    WHERE 
        directors IN (
            SELECT DISTINCT directors 
            FROM top10_audience_movies
        );
    """
]

# Framkvæma allar fyrirspurnirnar
for query in queries:
    cursor.execute(query)

# Loka tengingu
conn.commit()
conn.close()