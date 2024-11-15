import sqlite3
from imdb import Cinemagoer
import time

# Tengjast SQLite gagnagrunninum
db_path = "data/rotten_tomatoes.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


# Eyða töflunni ef hún er til og búa hana til á ný
cursor.execute("DROP TABLE IF EXISTS actors_info;")
cursor.execute("""
    CREATE TABLE actors_info (
        imdbID TEXT PRIMARY KEY,
        name TEXT,
        headshot TEXT,
        mini_biography TEXT,
        canonical_name TEXT,
        long_imdb_name TEXT,
        long_imdb_canonical_name TEXT,
        full_size_headshot TEXT
    );
""")

# Tengjast IMDb með Cinemagoer
ia = Cinemagoer()

# Tryggjum að Leonardo DiCaprio og Kate Winslet séu alltaf í listanum
important_actors = ['Leonardo DiCaprio', 'Kate Winslet']

# Fall til að bæta leikara við töfluna með staðfestingu út frá kvikmyndatitli
def add_actor_to_table(actor_name, movie_title):
    print(f"Vinnsla hafin fyrir {actor_name} í myndinni '{movie_title}'")
    try:
        # Leita að leikaranum í IMDb gagnagrunninum
        persons = ia.search_person(actor_name)
        
        if persons:
            for person in persons:
                # Fá IMDb ID fyrir leikara
                imdb_id = person.personID
                person_data = ia.get_person(imdb_id)
                
                # Athuga hvort leikarinn er skráður í rétta kvikmynd á IMDb
                imdb_movies = {movie['title'] for movie in person_data.get('filmography', {}).get('actor', [])}
                
                if movie_title in imdb_movies:
                    print(f"Skrái upplýsingar fyrir {actor_name} (IMDb ID: {imdb_id}) tengdan myndinni '{movie_title}'")
                    # Setja saman gögn fyrir nýja færslu ef kvikmyndatitill passar
                    actor_info = (
                        imdb_id,
                        person_data.get('name'),
                        person_data.get('headshot'),
                        person_data.get('mini biography', [''])[0],  # Fær fyrsta atriði ef til
                        person_data.get('canonical name'),
                        person_data.get('long imdb name'),
                        person_data.get('long imdb canonical name'),
                        person_data.get('full-size headshot')
                    )

                    # Setja gögnin inn í actors_info töfluna
                    cursor.execute("""
                        INSERT OR IGNORE INTO actors_info (imdbID, name, headshot, mini_biography, canonical_name, 
                                                           long_imdb_name, long_imdb_canonical_name, full_size_headshot)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, actor_info)

                    # Uppfæra actor_id í movie_actors með IMDb ID fyrir réttan leikara
                    cursor.execute("""
                        UPDATE movie_actors
                        SET actor_id = ?
                        WHERE actor_name = ? 
                          AND movie_id IN (
                              SELECT rt.movie_id 
                              FROM rotten_tomatoes_movies_dicaprio_winslet AS rt
                              WHERE rt.movie_title = ?
                          ) 
                          AND (actor_id IS NULL OR actor_id = '')
                    """, (imdb_id, actor_name, movie_title))

                    print(f"IMDb ID fyrir {actor_name} hefur verið uppfært í movie_actors")
                    
                    # Bæta við smá töf til að forðast API takmörkun
                    time.sleep(0.1)
                    return  # Ef rétta kvikmynd finnst, hætta leitarferli fyrir þennan leikara

    except Exception as e:
        print(f"Villa kom upp við vinnslu leikara {actor_name}: {e}")

# Bæta Leonardo DiCaprio og Kate Winslet fyrst inn í töfluna
for actor_name in important_actors:
    cursor.execute("""
        SELECT ma.movie_id, rt.movie_title 
        FROM rotten_tomatoes_movies_dicaprio_winslet AS rt
        JOIN movie_actors AS ma ON rt.movie_id = ma.movie_id
        WHERE ma.actor_name = ?
    """, (actor_name,))
    movies = cursor.fetchall()
    for movie_id, movie_title in movies:
        add_actor_to_table(actor_name, movie_title)

# Sækja aðra leikara (með limit á 10)
cursor.execute("""
    SELECT DISTINCT ma.actor_name, ma.movie_id 
    FROM movie_actors AS ma
    WHERE ma.actor_name NOT IN ('Leonardo DiCaprio', 'Kate Winslet')
    LIMIT 8
""")
additional_actors = cursor.fetchall()

# Bæta við leikarum með kvikmyndatengingu
for actor_name, movie_id in additional_actors:
    cursor.execute("""
        SELECT rt.movie_title 
        FROM rotten_tomatoes_movies_dicaprio_winslet AS rt
        WHERE rt.movie_id = ?
    """, (movie_id,))
    movie_title = cursor.fetchone()[0]
    add_actor_to_table(actor_name, movie_title)

# Vista breytingarnar og loka tengingunni
conn.commit()
conn.close()

print("Gögn fyrir alla mikilvæga leikara hafa verið sótt og vistuð í 'actors_info' töfluna og 'actor_id' hefur verið uppfært í 'movie_actors' fyrir hvern leikara.")