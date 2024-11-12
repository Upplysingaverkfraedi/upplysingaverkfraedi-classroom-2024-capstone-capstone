import sqlite3
import re

# Breyta gildum í genres dálkinum í töflunni rotten_tomatoes_movies_dicaprio_winslet
# Tengist gagnagrunninum rotten_tomatoes.db
conn = sqlite3.connect('data/rotten_tomatoes.db')
cursor = conn.cursor()

# Skilgreinir lista af æskilegum flokkum
valid_genres = ['Drama', 'Mystery & Suspense', 'Action & Adventure', 'Romance', 'Documentary']

# Function til að hreinsa genres dálkinn
def clean_genres(genres):
    # Finnur æskilega flokka í genres dálknum
    found_genres = [genre for genre in valid_genres if genre in genres]
    
    # Ef það eru aðrir flokkar, bætir við "Other"
    if len(found_genres) < len(genres.split(', ')):
        found_genres.append("Other")
    
    return ', '.join(found_genres)

# Velur gögn úr töflunni
cursor.execute("SELECT rowid, genres FROM rotten_tomatoes_movies_dicaprio_winslet")
rows = cursor.fetchall()

# Uppfærir genres dálkinn með hreinsuðum gildum
for row in rows:
    rowid, genres = row
    updated_genres = clean_genres(genres)
    cursor.execute("UPDATE rotten_tomatoes_movies_dicaprio_winslet SET genres = ? WHERE rowid = ?", (updated_genres, rowid))

# Geymir breytingar í gagnagrunninum
conn.commit()

# Loka tengingu
conn.close()

print("Genres dálkurinn hefur verið uppfærður!")