import requests
import pandas as pd
import argparse
import re
from datetime import datetime
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description='Scrape beer prices from Vinbudin website.')
    parser.add_argument('--url', help='URL of the website to scrape.', default="https://www.vinbudin.is/heim")
    parser.add_argument('--output_dir', default='data', help='Directory to save the results.')
    parser.add_argument('--debug', action='store_true', help='Save HTML to a file for debugging.')
    return parser.parse_args()


def fetch_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Tókst ekki að sækja gögn af {url}")
        return None
    
def parse_html(html):
    """
    Vinnur úr HTML gögnum og skilar lista af niðurstöðum og upplýsingum um hlaupið.
    """
    # Regex to match both beer names and prices in the format found on the Vinbudin site
    # Example pattern (this may need adjustment based on actual HTML structure):
    # r'<div class="product-name">([^<]+)</div>.*?(\d{1,3}(?:\.\d{3})* kr)'
    beer_pattern = r'<span id="ctl00_ctl01_Label_ProductName" class="product-info-text">([^<]+)</span>.*?<span id="ctl00_ctl01_Label_ProductPrice" class="money">([\d.,]+)</span>'


    matches = re.findall(beer_pattern, html, re.DOTALL)

    if not matches:
        print("No beer names or prices found in the HTML.")
        return []

    # Clean up prices and store names and prices in a list of dictionaries
    beers_data = [{"Name": name.strip(), "Price (ISK)": price.replace(" kr", "").replace(".", "")} for name, price in matches]
    return beers_data



def save_results(beers_data, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    filename = f"beer_prices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = os.path.join(output_dir, filename) #filename (_beer_prices_)
    
    df = pd.DataFrame(beers_data, columns=["Beer","Price (ISK)"])
    df.to_csv(filepath, index=False)
    print(f"Prices saved to {filepath}")

if __name__ == "__main__":
    args = parse_arguments()
    html = fetch_html(args.url)

    if html:
        # Gætir þess að output directory er til
        os.makedirs(args.output_dir, exist_ok=True)

        # Save debug HTML file hjá okkur
        if args.debug:
            with open(os.path.join(args.output_dir, 'debug.html'), 'w') as f:
                f.write(html)
        
        # Parse HTML and retrieve beer data
        beers_data = parse_html(html)  # Changed from 'prices' to 'beers_data'
        save_results(beers_data, args.output_dir)  # Updated to use 'beers_data'




#python REGEX_Vinbudin_kodi.py --url "https://www.vinbudin.is/heim/vorur/stoek-vara.aspx/?productid=21456/" --output_dir ./data --debug
