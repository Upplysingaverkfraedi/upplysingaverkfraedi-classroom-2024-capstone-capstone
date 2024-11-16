import sqlite3
import pandas as pd
import requests
import time

# Tengist gagnagrunninum
DB_PATH = "f1db.db"

# Fáum lista yfir race_id, grand_prix_id og circuit_id
def get_race_data():
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT h.race_id, r.grand_prix_id, r.circuit_id
    FROM hamilton_verstappen_all_time_data AS h
    JOIN race AS r ON h.race_id = r.id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.drop_duplicates(subset=['race_id'])  # Fjarlægir tvítekningar

# Finna hnit með Nominatim API með villumeðhöndlun
def get_coordinates_nominatim(location_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location_name,        # Nafn staðarins sem þú vilt leita að
        "format": "json",           # JSON skilaformat
        "limit": 1,                 # Takmörkun við eina niðurstöðu
        "addressdetails": 1         # Inniheldur upplýsingar um staðsetningu
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Athugar fyrir HTTP villur (t.d. 404 eða 500)
        
        # Athugar hvort svarið er tómt eða inniheldur gögn
        if response.text.strip():    # Sannar ef textinn er ekki tómur
            data = response.json()   # Reynir að afkóða JSON gögnin
            if data:                 # Athugar hvort JSON gögnin innihalda upplýsingar
                lat = data[0]["lat"]
                lon = data[0]["lon"]
                return float(lat), float(lon)
            else:
                print(f"No results found for location: {location_name}")
        else:
            print(f"Empty response for location: {location_name}")
    
    except requests.exceptions.RequestException as e:
        print(f"Request failed for location: {location_name}. Error: {e}")
    
    return None, None

# Búa til nýja töflu með hnitum
def create_location_table():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS race_locations (
        race_id INTEGER PRIMARY KEY,
        grand_prix_id TEXT,
        circuit_id TEXT UNIQUE,
        lat REAL,
        lon REAL
    )
    """)
    conn.close()

# Athuga hvort circuit_id er nú þegar til í töflunni
def circuit_exists(circuit_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM race_locations WHERE circuit_id = ?", (circuit_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

# Setur gögn í töfluna race_locations
def insert_location_data(race_id, grand_prix_id, circuit_id, lat, lon):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
    INSERT OR REPLACE INTO race_locations (race_id, grand_prix_id, circuit_id, lat, lon)
    VALUES (?, ?, ?, ?, ?)
    """, (race_id, grand_prix_id, circuit_id, lat, lon))
    conn.commit()
    conn.close()

# Aðalforritið
def main():
    # Fáum öll gögn úr töflunni
    race_data = get_race_data()
    
    # Búa til nýju töfluna ef hún er ekki til
    create_location_table()
    
    # Fara í gegnum hverja röð og finna hnit
    for index, row in race_data.iterrows():
        race_id = row['race_id']
        grand_prix_id = row['grand_prix_id']
        circuit_id = row['circuit_id']
        
        # Sleppa ef circuit_id er nú þegar til í race_locations
        if circuit_exists(circuit_id):
            print(f"Circuit ID {circuit_id} already exists, skipping.")
            continue
        
        # Nota circuit_id til að fá hnit með OpenStreetMap Nominatim API
        lat, lon = get_coordinates_nominatim(circuit_id)
        
        if lat is not None and lon is not None:
            # Setja gögnin inn í nýju töfluna
            insert_location_data(race_id, grand_prix_id, circuit_id, lat, lon)
            print(f"Added {circuit_id} with lat: {lat}, lon: {lon}")
        
        # Bæta við 1 sekúndu töf til að fylgja reglum OpenStreetMap
        time.sleep(1)

# Keyra forritið
main()
