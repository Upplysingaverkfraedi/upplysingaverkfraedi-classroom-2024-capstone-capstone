import sqlite3
import requests
from bs4 import BeautifulSoup
import re

# Step 1: Tengjast SQLite gagnagrunninum
db_path = "f1db.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Eyða töflunni ef hún er til og endurskapa hana
cursor.execute("DROP TABLE IF EXISTS race_data")
cursor.execute("""
CREATE TABLE race_data (
    race_id INTEGER,
    driver_id TEXT,
    lap INTEGER,
    fastest_time TIME,
    avg_speed REAL,
    pit_stops INTEGER,
    pit_lap INTEGER,
    pit_time TIME
)
""")
conn.commit()
print("1. Tengdur við gagnagrunninn. Tafla 'race_data' eytt og endursköpuð.")

# Step 2: Sækja gögn frá Formula 1 vefsíðunni
base_url = "https://www.formula1.com/en/results/2021/races.html"
print(f"2. Sækir gögn frá {base_url}...")
response = requests.get(base_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Example race_mapping for demonstration (fylltu inn raunveruleg gögn)
race_mapping = {
    "Bahrain": 1036,
    "Emilia-Romagna": 1037,
    "Portugal": 1038,
    "Spain": 1039,
    "Monaco": 1040,
    "Azerbaijan": 1041,
    "France": 1042,
    "Styria": 1043,
    "Austria": 1044,
    "Great Britain": 1045,
    "Hungary": 1046,
    "Belgium": 1047,
    "Netherlands": 1048,
    "Italy": 1049,
    "Russia": 1050,
    "Turkey": 1051,
    "United States": 1052,
    "Mexico": 1053,
    "Brazil": 1054,
    "Qatar": 1055,
    "Saudi Arabia": 1056,
    "Abu Dhabi": 1057
}
print(f"3. Notar race_mapping: {list(race_mapping.keys())}")

# Nota regex til að finna tengla fyrir hvert Grand Prix
race_links = {}
for name, race_id in race_mapping.items():
    link_tag = soup.find('a', string=re.compile(name, re.IGNORECASE))
    if link_tag and 'href' in link_tag.attrs:
        race_links[race_id] = link_tag['href']
        print(f"   - Finnur tengil fyrir {name}: {link_tag['href']}")

# Step 3: Sækja gögn fyrir hvert race
drivers = {'lewis-hamilton': 'Lewis Hamilton', 'max-verstappen': 'Max Verstappen'}

for race_id, race_url in race_links.items():
    print(f"\n4. Sækir gögn fyrir keppni {race_id} á {race_url}...")
    race_response = requests.get(f"https://www.formula1.com{race_url}")
    race_soup = BeautifulSoup(race_response.text, 'html.parser')
    print("   - Prenta hluta af HTML innihaldi keppninnar...")
    print(race_soup.prettify()[:500])  # Prenta fyrstu 500 stafi

    # Sækir gögn úr "Fastest Laps"
    print("   - Leitar að töflu 'Fastest Laps'...")
    fastest_laps_table = race_soup.find('table', string=re.compile("Fastest Laps", re.IGNORECASE))
    if fastest_laps_table:
        print("     -> Tafla 'Fastest Laps' fundin.")
        for row in fastest_laps_table.find_all('tr')[1:]:  # Sleppa haus
            cols = row.find_all('td')
            if len(cols) >= 5:
                driver_name = cols[1].text.strip()
                driver_id = [k for k, v in drivers.items() if v.lower() in driver_name.lower()]
                if driver_id:
                    lap = int(cols[0].text.strip())
                    fastest_time = cols[2].text.strip()
                    avg_speed = float(cols[3].text.strip())
                    print(f"       - {driver_name}: Hringur {lap}, Tími {fastest_time}, Meðalhraði {avg_speed} km/klst.")

                    # Setur í gagnagrunn
                    print(f"Set í töflu: race_id={race_id}, driver_id={driver_id[0]}, lap={lap}, time={fastest_time}, avg_speed={avg_speed}")
                    cursor.execute("""
                        INSERT INTO race_data (race_id, driver_id, lap, fastest_time, avg_speed)
                        VALUES (?, ?, ?, ?, ?)
                    """, (race_id, driver_id[0], lap, fastest_time, avg_speed))
    else:
        print("     -> Tafla 'Fastest Laps' ekki fundin.")

    # Sækir gögn úr "Pit stop summary"
    print("   - Leitar að töflu 'Pit stop summary'...")
    pit_stop_table = race_soup.find('table', string=re.compile("Pit stop summary", re.IGNORECASE))
    if pit_stop_table:
        print("     -> Tafla 'Pit stop summary' fundin.")
        for row in pit_stop_table.find_all('tr')[1:]:  # Sleppa haus
            cols = row.find_all('td')
            if len(cols) >= 4:
                driver_name = cols[1].text.strip()
                driver_id = [k for k, v in drivers.items() if v.lower() in driver_name.lower()]
                if driver_id:
                    pit_stops = int(cols[0].text.strip())
                    pit_lap = int(cols[2].text.strip())
                    pit_time = cols[3].text.strip()
                    print(f"       - {driver_name}: Stoppar {pit_stops} sinnum, á hring {pit_lap}, Tími {pit_time}.")

                    # Setur í gagnagrunn
                    print(f"Set í töflu: race_id={race_id}, driver_id={driver_id[0]}, pit_stops={pit_stops}, pit_lap={pit_lap}, pit_time={pit_time}")
                    cursor.execute("""
                        INSERT INTO race_data (race_id, driver_id, pit_stops, pit_lap, pit_time)
                        VALUES (?, ?, ?, ?, ?)
                    """, (race_id, driver_id[0], pit_stops, pit_lap, pit_time))
    else:
        print("     -> Tafla 'Pit stop summary' ekki fundin.")

    conn.commit()

# Lokar tengingu við gagnagrunn
conn.close()
print("\nKeyrslu lokið. Gögn vistuð í gagnagrunninn.")
