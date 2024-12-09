# utils/scraper.py
import requests
import pandas as pd
from bs4 import BeautifulSoup
from config.config import Config

class IPOScraper:
    @staticmethod
    def scrape_ipo_data():
        try:
            response = requests.get(Config.IPO_URL)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            table = soup.find('table')
            df = pd.read_html(str(table))[0]
            
            df.columns = ['Current IPOs', 'IPO GMP', 'IPO Price', 'Gain', 
                         'Kostak', 'Subject', 'Type']
            
            # Clean data
            df['Gain'] = df['Gain'].str.rstrip('%').astype(float)
            df['Current IPOs'] = df['Current IPOs'].str.split('\n').str[0]
            df['Date'] = df['Current IPOs'].str.extract(
                r'(\d{1,2}-\d{1,2}\s*(?:Dec|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov))')
            
            return df
        except Exception as e:
            print(f"Error scraping data: {str(e)}")
            return None
