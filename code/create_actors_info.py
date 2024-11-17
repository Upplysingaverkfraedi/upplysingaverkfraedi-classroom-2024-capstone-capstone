import sqlite3
from imdb import Cinemagoer
import time

# Tengjast SQLite gagnagrunninum
conn = sqlite3.connect('data/rotten_tomatoes.db')
cursor = conn.cursor()

# Búa til actors_info töfluna ef hún er ekki til, og eyða henni ef hún er nú þegar til
#cursor.execute("DROP TABLE IF EXISTS actors_info;")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS actors_info (
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

# Sækja einstaka nöfn úr movie_actors töflunni án takmörkunar
# Getur byrjað á að setja: SELECT DISTINCT actor_name FROM movie_actors LIMIT 10 inní þennan glugga: 
cursor.execute("SELECT DISTINCT actor_name FROM movie_actors WHERE actor_id IS NULL limit 100") 
actor_names = [row[0] for row in cursor.fetchall()]

# Fyrir hvern einstakan leikara, sækja upplýsingar frá Cinemagoer
for I, actor_name in enumerate(actor_names):
    print(I, actor_name)
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
                INSERT OR IGNORE INTO actors_info (imdbID, name, headshot, mini_biography, canonical_name, 
                                                   long_imdb_name, long_imdb_canonical_name, full_size_headshot)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, actor_info)
            # update movie_actors with imdb value for column actor_id where name = actor_name
            imdb = actor_info[0]
            cursor.execute("UPDATE movie_actors SET actor_id = ? WHERE actor_name = ?", (imdb,  actor_name))



            # Taka smá töf til að forðast API takmörkun
            time.sleep(0.1)  # Stillt á 0.1 sekúndu sem dæmi

    except Exception as e:
        print(f"Villa kom upp við vinnslu leikara {actor_name}: {e}")


# Vista breytingarnar og loka tengingunni
conn.commit()
conn.close()