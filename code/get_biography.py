import sqlite3
import requests
from bs4 import BeautifulSoup
import re

# Tengist gagnagrunninum
conn = sqlite3.connect('data/rotten_tomatoes.db')
cursor = conn.cursor()

# Athugar hvort dálkur er þegar til
def add_column_if_not_exists(table_name, column_name, column_type):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]
    if column_name not in columns:
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
        print(f"Dálkur '{column_name}' bætt við töfluna '{table_name}'.")

# Bætir við nýjum dálkum ef þeir eru ekki til
add_column_if_not_exists("actors_info", "mini_biography", "TEXT")
add_column_if_not_exists("actors_info", "trivia_1", "TEXT")
add_column_if_not_exists("actors_info", "trivia_2", "TEXT")
add_column_if_not_exists("actors_info", "highest_paid_movie", "TEXT")
add_column_if_not_exists("actors_info", "highest_salary", "INTEGER")

# Stillir User-Agent
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
}

# Hreinsar texta áður en hann er geymdur í gagnagrunninum
def clean_text_for_db(text):
    if not text:
        return None
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    text = re.sub(r'([0-9])([A-Za-z])', r'\1 \2', text)
    text = re.sub(r'([A-Za-z])([0-9])', r'\1 \2', text)
    text = re.sub(r'([a-zA-Z])\(', r'\1 (', text)
    text = re.sub(r'\)([a-zA-Z])', r') \1', text)
    text = re.sub(r'([a-zA-Z])and', r'\1 and', text)
    text = re.sub(r'\bDi Caprio\b', 'DiCaprio', text)
    text = re.sub(r'\bDi Caprioas\b', 'DiCaprio as', text)
    return text

# Sækir lista yfir leikara og IMDb ID úr actors_info
cursor.execute("SELECT actor_name, imdb_id FROM actors_info WHERE imdb_id IS NOT NULL")
actors = cursor.fetchall()  # Skilar [(actor_name, imdb_id), ...]

for actor_name, imdb_id in actors:
    try:
        print(f"Sæki gögn fyrir: {actor_name} ({imdb_id})")

        # IMDb slóð fyrir Mini Bio og Salary
        url = f"https://www.imdb.com/name/nm{imdb_id}/bio/?ref_=nm_ov_bio_sm#mini_bio"

        # Sækir HTML efni
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Leitar að Mini Bio
            mini_bio_section = soup.find('div', {"data-testid": "sub-section-mini_bio"})
            mini_bio_text = mini_bio_section.get_text(strip=True) if mini_bio_section else None

            if mini_bio_text:
                sentences = re.findall(r'[^.!?]+[.!?]', mini_bio_text)
                mini_bio_text = ' '.join(sentences[:5])  # Tekur fyrstu 5 setningarnar

            # Hreinsar Mini Bio
            mini_bio_text = clean_text_for_db(mini_bio_text)

            # Leitar að Trivia hlutum
            trivia_texts = []
            for i in range(2):
                trivia_section = soup.find('li', {"id": f"trivia_{i}"})
                if trivia_section:
                    trivia_content = trivia_section.find('div', class_='ipc-html-content-inner-div')
                    if trivia_content:
                        trivia_text = trivia_content.get_text(strip=True)
                        trivia_text = clean_text_for_db(trivia_text)  # Hreinsar trivia
                        trivia_texts.append(trivia_text)
                    else:
                        trivia_texts.append(None)
                else:
                    trivia_texts.append(None)

            # Leitar að Salary hlutum
            salary_section = soup.find('div', {"data-testid": "sub-section-salary"})
            highest_paid_movie = "Not Specified"
            highest_salary = 0
            if salary_section:
                salaries = salary_section.find_all('li', {"data-testid": "list-item"})
                for salary in salaries:
                    salary_text = salary.get_text(strip=True)
                    match = re.search(r'^(.*) - [\$£€]?([\d,]+)', salary_text)
                    if match:
                        movie_name = match.group(1).strip()
                        movie_name = re.sub(r'\((\d{4})\)', r' (\1)', movie_name)  # Bætir við bili fyrir ár
                        salary_amount = int(match.group(2).replace(',', ''))
                        if salary_amount > highest_salary:
                            highest_salary = salary_amount
                            highest_paid_movie = movie_name

            # Uppfærir gögn í gagnagrunninum
            cursor.execute("""
                UPDATE actors_info
                SET mini_biography = ?, trivia_1 = ?, trivia_2 = ?, highest_paid_movie = ?, highest_salary = ?
                WHERE imdb_id = ?
            """, (mini_bio_text, trivia_texts[0], trivia_texts[1], highest_paid_movie, highest_salary, imdb_id))
            conn.commit()  # Staðfestir breytingar

            print(f"Gögn uppfærð fyrir: {actor_name} ({imdb_id}) - Highest Paid Movie: {highest_paid_movie}, Salary: {highest_salary}")
        else:
            print(f"Villa við að sækja gögn fyrir: {actor_name} ({imdb_id}), HTTP Status: {response.status_code}")

    except Exception as e:
        print(f"Villa kom upp við vinnslu leikara {actor_name} ({imdb_id}): {e}")

# Loka tengingu
conn.close()
print("Allar upplýsingar hafa verið uppfærðar.")