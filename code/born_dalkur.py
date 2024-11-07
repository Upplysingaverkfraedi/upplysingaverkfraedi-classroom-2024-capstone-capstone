import sqlite3
import re
from imdb import Cinemagoer
import time

# Tengjast SQLite gagnagrunninum
conn = sqlite3.connect('data/rotten_tomatoes.db')
cursor = conn.cursor()

# Bæta við dálknum born ef hann er ekki til
cursor.execute("ALTER TABLE actors_info ADD COLUMN born TEXT;")

# Regex til að finna fæðingardagsetningu í "Simon McBurney was born on August 25, 1957" formi
date_regex = re.compile(r'\b(?:was born on|born on|born)\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})')

# Sækja öll gögn úr actors_info til að uppfæra born dálkinn
cursor.execute("SELECT imdbID, mini_biography FROM actors_info")
rows = cursor.fetchall()

# Farðu í gegnum hverja færslu og finndu dagsetningu með regex
for imdbID, mini_bio in rows:
    if mini_bio:
        match = date_regex.search(mini_bio)
        if match:
            born_date = match.group(1)  # Sækja dagsetninguna úr regex hópnum
            # Uppfæra born dálkinn með fundinni dagsetningu
            cursor.execute("UPDATE actors_info SET born = ? WHERE imdbID = ?", (born_date, imdbID))

# Vista breytingar og loka tengingunni
conn.commit()
conn.close()