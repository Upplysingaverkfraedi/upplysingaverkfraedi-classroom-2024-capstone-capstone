import sqlite3
from imdb import Cinemagoer
import time

# Tengjast SQLite gagnagrunninum
conn = sqlite3.connect('data2/rotten_tomatoes.db')
cursor = conn.cursor()

# Búa til actors_info töfluna ef hún er ekki til, og eyða henni ef hún er nú þegar til
cursor.execute("DROP TABLE IF EXISTS actors_info1;")
cursor.execute("""
    CREATE TABLE actors_info1 (
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

# Tryggjum að Leonardo DiCaprio og Kate Winslet séu alltaf í listanum og fyllum upp í með fleiri leikurum
cursor.execute("""
    SELECT DISTINCT actor_name 
    FROM movie_actors 
    WHERE actor_name NOT IN ('Leonardo DiCaprio', 'Kate Winslet')
    LIMIT 8
""")
additional_actors = [row[0] for row in cursor.fetchall()]

# Bæta Leonardo DiCaprio og Kate Winslet í listann
actor_names = ['Leonardo DiCaprio', 'Kate Winslet'] + additional_actors

# Fyrir hvern einstakan leikara, sækja upplýsingar frá Cinemagoer
for actor_name in actor_names:
    try:
        # Leita að leikaranum í IMDb gagnagrunninum
        persons = ia.search_person(actor_name)
        
        # Velja fyrsta niðurstöðuna ef hún finnst
        if persons:
            person = ia.get_person(persons[0].personID)  # Sækja persónu með IMDb ID

            # Setja saman gögn fyrir nýja færslu
            actor_info = (
                person.personID,
                person.get('name'),
                person.get('headshot'),
                person.get('mini biography', [''])[0],  # Fær fyrsta atriði ef til
                person.get('canonical name'),
                person.get('long imdb name'),
                person.get('long imdb canonical name'),
                person.get('full-size headshot')
            )

            # Setja gögnin inn í actors_info töfluna
            cursor.execute("""
                INSERT OR IGNORE INTO actors_info1 (imdbID, name, headshot, mini_biography, canonical_name, 
                                                   long_imdb_name, long_imdb_canonical_name, full_size_headshot)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, actor_info)
            
            # Taka smá töf til að forðast API takmörkun
            time.sleep(0.1)  # Stillt á 0.1 sekúndu sem dæmi

    except Exception as e:
        print(f"Villa kom upp við vinnslu leikara {actor_name}: {e}")

# Vista breytingarnar og loka tengingunni
conn.commit()
conn.close()