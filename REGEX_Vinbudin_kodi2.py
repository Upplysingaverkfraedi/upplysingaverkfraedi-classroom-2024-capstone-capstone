import re
import requests
import pandas as pd
from datetime import datetime
import os

# Load URLs from a GitHub file link
def load_urls_from_github(github_url):
    response = requests.get(github_url)
    if response.status_code == 200:
        urls = [line.strip() for line in response.text.splitlines() if line.strip() and not line.startswith('#')]
        return urls
    else:
        print(f"Failed to retrieve URL list from {github_url}")
        return []

# Fetch the HTML from a URL
def fetch_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve data from {url}")
        return None

# Parse HTML using regex to extract beer names and prices separately
def parse_html(html):
    # Regex pattern for beer name and price
    beer_pattern = (
        r'<span id="ctl00_ctl01_Label_ProductName" class="product-info-text">([^<]+)</span>.*?'
        r'<span id="ctl00_ctl01_Label_ProductPrice" class="money">([\d.,]+)</span>'
    )

    # Regex pattern for volume in ml
    volume_pattern = r'<span[^>]*id="ctl00_ctl01_Label_ProductBottleVolumeMobile"[^>]*>(\d+)\s*ml</span>'

    # Find matches for beer name and price
    beer_matches = re.findall(beer_pattern, html, re.DOTALL)
    
    # Find match for volume
    volume_match = re.search(volume_pattern, html, re.DOTALL)

    if not beer_matches:
        print("No beer names or prices found in the HTML.")
        return []

    # If volume is found, extract it, otherwise set as 'Unknown'
    volume_ml = volume_match.group(1).strip() if volume_match else 'Unknown'

    # Process beer matches into a list of dictionaries, including volume
    beers_data = [{"Name": name.strip(), "Price (ISK)": price.replace(".", "").replace(",", ""), "ml": volume_ml} for name, price in beer_matches]
    
    return beers_data

# Save the results to a single CSV file
def save_results(all_beers_data, output_dir):
    if not all_beers_data:
        print("No data to save.")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    filename = f"beer_prices_.csv"
    filepath = os.path.join(output_dir, filename)

    df = pd.DataFrame(all_beers_data, columns=["Name", "Price (ISK)", "ml"])
    df.to_csv(filepath, index=False)
    print(f"Prices saved to {filepath}")

if __name__ == "__main__":
    # GitHub raw URL for the file containing URLs
    github_url = 'https://raw.githubusercontent.com/Upplysingaverkfraedi/capstone-thestormlands/REGEX_Vinbudin_Kronur/REGEX_Linkar.txt'
    urls = load_urls_from_github(github_url)

    output_dir = './data'
    all_beers_data = []

    for url in urls:
        html = fetch_html(url)
        if html:
            beers_data = parse_html(html)
            all_beers_data.extend(beers_data)

    if all_beers_data:
        save_results(all_beers_data, output_dir)
