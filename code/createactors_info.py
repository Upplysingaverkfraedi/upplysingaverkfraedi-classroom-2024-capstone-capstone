import sqlite3
from imdb import Cinemagoer
import unicodedata
import re
from difflib import get_close_matches

# Tengjast SQLite gagnagrunninum
db_path = "data/rotten_tomatoes.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Tengjast IMDb með Cinemagoer
ia = Cinemagoer()

# Tryggja að taflan actors_info sé til
cursor.execute("""
CREATE TABLE IF NOT EXISTS actors_info (
    actor_name TEXT NOT NULL,
    imdb_id TEXT NOT NULL PRIMARY KEY,
    headshot TEXT,
    canonical_name TEXT,
    long_imdb_name TEXT,
    long_imdb_canonical_name TEXT,
    full_size_headshot TEXT
);
""")
conn.commit()
print("Taflan 'actors_info' er tilbúin.")

# Athuga hvort dálkurinn 'processed' er þegar til í töflunni
cursor.execute("PRAGMA table_info(rotten_tomatoes_movies_dicaprio_winslet);")
columns = [row[1] for row in cursor.fetchall()]  # Fá lista yfir dálkanöfn

if 'processed' not in columns:
    cursor.execute("ALTER TABLE rotten_tomatoes_movies_dicaprio_winslet ADD COLUMN processed INTEGER DEFAULT 0;")
    conn.commit()
    print("Dálkurinn 'processed' bætt við töfluna.")
else:
    print("Dálkurinn 'processed' er þegar til í töflunni.")
conn.commit()

# Hreinsun á nöfnum
def normalize_name(name):
    """Hreinsar nafn með því að fjarlægja sérstafi, bil, sviga og breyta í lágstafi."""
    name = unicodedata.normalize('NFD', name)
    name = ''.join([c for c in name if unicodedata.category(c) != 'Mn'])  # Fjarlægir sérstafi
    name = re.sub(r'\s*\(.*?\)', '', name)  # Fjarlægir sviga og innihald
    return name.strip().lower()

# Fall til að skrá upplýsingar um leikara í actors_info
def save_actor_to_actors_info(imdb_person):
    """Skráir upplýsingar um leikara í actors_info ef ekki til."""
    cursor.execute("""
        INSERT OR IGNORE INTO actors_info (
            actor_name, imdb_id, headshot, canonical_name,
            long_imdb_name, long_imdb_canonical_name, full_size_headshot
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        imdb_person.get('name', None),
        imdb_person.personID,
        imdb_person.get('headshot', None),
        imdb_person.get('canonical name', None),
        imdb_person.get('long imdb name', None),
        imdb_person.get('long imdb canonical name', None),
        imdb_person.get('full-size headshot', None)
    ))
    conn.commit()

# Fall til að meðhöndla hverja kvikmynd
def process_movie(movie_id, movie_title):
    print(f"\nVinnsla kvikmyndar með ID: {movie_id}, Titill: {movie_title}")

    # Sækja IMDb ID fyrir myndina
    movie = ia.search_movie(movie_title)
    if not movie:
        print(f"IMDb mynd fannst ekki fyrir titil: {movie_title}")
        return
    imdb_movie = movie[0]
    imdb_movie_id = imdb_movie.movieID
    print(f"IMDb ID fundið fyrir {movie_title}: {imdb_movie_id}")

    # Sækja allt cast úr IMDb
    movie_details = ia.get_movie(imdb_movie_id)
    if not movie_details or 'cast' not in movie_details:
        print(f"Enginn cast listi fundinn fyrir {movie_title}")
        return
    cast = movie_details['cast']

    # Sækja actor_name úr movie_actors fyrir þetta movie_id
    cursor.execute("SELECT actor_name FROM movie_actors WHERE movie_id = ?", (movie_id,))
    actor_names = [row[0] for row in cursor.fetchall()]
    normalized_actor_names = [normalize_name(name) for name in actor_names]
    print(f"Leikarar úr gagnagrunninum (normalíserað): {normalized_actor_names}")

    # Bera saman actor_name og IMDb cast
    unmatched_actors = []
    for cast_member in cast:
        imdb_name = normalize_name(cast_member['name'])
        matches = get_close_matches(imdb_name, normalized_actor_names, n=1, cutoff=0.8)

        if matches:
            matched_name = matches[0]
            actor_imdb_id = cast_member.personID

            print(f"Passandi leikari: {imdb_name} -> {matched_name}, IMDb ID: {actor_imdb_id}")

            # Sækja frekari upplýsingar um leikara úr IMDb
            imdb_person = ia.get_person(actor_imdb_id)
            if imdb_person:
                save_actor_to_actors_info(imdb_person)

            # Uppfæra movie_actors með IMDb ID leikara
            cursor.execute("""
                UPDATE movie_actors
                SET actor_id = ?
                WHERE movie_id = ? AND LOWER(actor_name) = ?
            """, (actor_imdb_id, movie_id, matched_name))
            conn.commit()

            # Fjarlægja nafnið úr listanum til að merkja sem uppfært
            normalized_actor_names.remove(matched_name)
        else:
            unmatched_actors.append(cast_member['name'])

    # Merkja kvikmynd sem unnin
    cursor.execute("""
        UPDATE rotten_tomatoes_movies_dicaprio_winslet
        SET processed = 1
        WHERE movie_id = ?
    """, (movie_id,))
    conn.commit()

    print(f"Leikarar sem fundust ekki: {unmatched_actors}")

# Skref 1: Fá óunnar kvikmyndir
cursor.execute("""
    SELECT DISTINCT ma.movie_id, rtm.movie_title
    FROM movie_actors ma
    JOIN rotten_tomatoes_movies_dicaprio_winslet rtm
    ON ma.movie_id = rtm.movie_id
    WHERE ma.movie_id IS NOT NULL AND rtm.processed = 0
""")
movies = cursor.fetchall()

# Skref 2-5: Keyra fyrir allar óunnar kvikmyndir
for movie_id, movie_title in movies:
    process_movie(movie_id, movie_title)

# Loka tengingu
conn.close()
print("Gögn hafa verið uppfærð.")