import re
import requests
import pandas as pd
from datetime import datetime
import os


# Load URL fyrir bjóra
def load_urls_from_file(file_name):

    # lesa skrá 'REGEX_Linkar.txt' sem inniheldir linka að "vefsíðum"
    with open(file_name, 'r') as file:
        urls =  [line.strip() for line in file if line.strip() and not line.startswith('#')]
        return urls
    
def fetch_html(url):  # Nær í url

    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        return html
    else:
        print(f"Náði ekki upplýsingum {url}")
        return None

# HTML
def parse_html(html):
    # Regex pattern fyrir bjór, Verð og ml

    beer_pattern = (
        r'<span id="ctl00_ctl01_Label_ProductName" class="product-info-text">([^<]+)</span>.*?'
        r'<span id="ctl00_ctl01_Label_ProductPrice" class="money">([\d.,]+)</span>'
    )
    volume_pattern = r'<span[^>]*id="ctl00_ctl01_Label_ProductBottleVolumeMobile"[^>]*>(\d+)\s*ml</span>' # Bæta við regex pattern fyrir volume in ml
    
    beer_matches = re.findall(beer_pattern, html, re.DOTALL) # Finna matches fyrir bjór, Verð og ml
    
    # Bæta við, finna match fyrir ml
    volume_match = re.search(volume_pattern, html, re.DOTALL) # Bætti þessum kóða við, sem rúmmáli ml seinna hér.

    if not beer_matches:
        print("Engin bjór, verð né ml fundið í HTML.")
        return []

    # Ef volume er fundið, extract it, otherwise set as 'Unknown'
    volume_ml = volume_match.group(1).strip() if volume_match else 'Unknown' 

    # Process beer matches í lista af dictionaries, including volume
    beers_data = [{"Bjór": name.strip(), "Verð (Kr)": price.replace(".", "").replace(",", ""), "Stærð (ml)": volume_ml} for name, price in beer_matches]

    return beers_data

# Save the results sem .CSV file
def save_results(all_beers_data, output_dir):
    if not all_beers_data:
        print("No data to save.") # Ef það er ekki fundið neitt í html vinbudin.is þá prentast þetta
        return
    
    os.makedirs(output_dir, exist_ok=True)
    filename = "Bjor_Vinbudin.csv"  # Nafn á CSV skrá
    filepath = os.path.join(output_dir, filename)

    df = pd.DataFrame(all_beers_data, columns=["Bjór", "Verð (Kr)", "Stærð (ml)"]) # Setja form .csv skjals þar sem efstu colums hafn merkingar
    df.to_csv(filepath, index=False)
    print(f"Verð vistað í {filepath}")

if __name__ == "__main__":
    # URL
    url_file = 'REGEX_Linkar.txt' # Nafn skjal með linkum
    urls = load_urls_from_file(url_file) # Keyra/load linkana

    output_dir = './data' # skjal sem heitir data
    all_beers_data = [] # Tómt skjal sem hefur allar upplýsingar um nafn bjór, verð og volume.

    for url in urls:
        html = fetch_html(url)
        if html:
            beers_data = parse_html(html) # notar fall def parse_html til að finna nafn, verð og ml
            all_beers_data.extend(beers_data) # Bætir beers_data við all_beers_data

    if all_beers_data: # Vistar upplýnsingar in í skjal data

        save_results(all_beers_data, output_dir)