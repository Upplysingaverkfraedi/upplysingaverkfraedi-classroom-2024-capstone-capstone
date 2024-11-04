import re
import requests
import pandas as pd
from datetime import datetime
import os

# Load URLs from a GitHub file link
def load_urls_from_github(github_url):
    response = requests.get(github_url)
    if response.status_code == 200:
        # Split lines and filter out empty or commented lines
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