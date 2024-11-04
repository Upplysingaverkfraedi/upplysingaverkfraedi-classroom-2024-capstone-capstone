import re
import requests
import pandas as pd
from datetime import datetime
import os

# Load URLs from the provided file
def load_urls(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip() and not line.startswith('#')]
    return urls

# Fetch the HTML from a URL
def fetch_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve data from {url}")
        return None

# Parse HTML using regex to extract beer names and prices
def parse_html(html):
    beer_pattern = (
        r'<span id="ctl00_ctl01_Label_ProductName" class="product-info-text">([^<]+)</span>.*?'
        r'<span id="ctl00_ctl01_Label_ProductPrice" class="money">([\d.,]+)</span>'
    )
    matches = re.findall(beer_pattern, html, re.DOTALL)

    if not matches:
        print("No beer names or prices found in the HTML.")
        return []

    beers_data = [{"Name": name.strip(), "Price (ISK)": price.replace(".", "").replace(",", "")} for name, price in matches]
    return beers_data

# Save the results to a single CSV file
def save_results(all_beers_data, output_dir):
    if not all_beers_data:
        print("No data to save.")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    filename = f"beer_prices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = os.path.join(output_dir, filename)

    df = pd.DataFrame(all_beers_data, columns=["Name", "Price (ISK)"])
    df.to_csv(filepath, index=False)
    print(f"Prices saved to {filepath}")

if __name__ == "__main__":
    # Path to the file containing URLs
    url_file = r'C:\Users\halld\Downloads\Háskóli_Íslands\Fjórða_ár_Haust_2024\IÐN302G\LokaverkefniStormlands\capstone-thestormlands\REGEX_Linkar.txt'
    urls = load_urls(url_file)

    output_dir = './data'
    all_beers_data = []

    for url in urls:
        html = fetch_html(url)
        if html:
            beers_data = parse_html(html)
            all_beers_data.extend(beers_data)

    if all_beers_data:
        save_results(all_beers_data, output_dir)
