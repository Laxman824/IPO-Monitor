# utils/scraper.py
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import time
from config.config import Config

class IPOScraper:
    @staticmethod
    def scrape_ipo_data():
        try:
            # Add headers to mimic a browser request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # Make the request with headers
            response = requests.get(Config.IPO_URL, headers=headers, timeout=10)
            response.raise_for_status()  # Raise an error for bad status codes
            
            # Print response status and first few characters for debugging
            print(f"Response status: {response.status_code}")
            print(f"Response preview: {response.text[:200]}")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try to find table with more specific selectors
            table = soup.find('table', {'class': ['wp-block-table', 'table']})
            if not table:
                print("Trying alternative table finding methods...")
                tables = soup.find_all('table')
                if tables:
                    table = tables[0]  # Get the first table if multiple exist
                
            if table:
                # Convert table to string and wrap with StringIO
                table_str = StringIO(str(table))
                
                try:
                    # Try parsing with different parsers
                    df = pd.read_html(table_str, flavor='bs4')[0]
                except Exception as e:
                    print(f"First parsing attempt failed: {e}")
                    try:
                        df = pd.read_html(str(table), flavor='html5lib')[0]
                    except Exception as e2:
                        print(f"Second parsing attempt failed: {e2}")
                        return None
                
                # Print raw dataframe for debugging
                print("Raw DataFrame:")
                print(df.head())
                
                # Clean and standardize column names
                # Updated to match current website structure
                expected_columns = ['Current IPOs', 'IPO GMP', 'IPO Price', 'Gain', 'Date']
                
                if len(df.columns) >= len(expected_columns):
                    df.columns = expected_columns
                    
                    # Data cleaning for new format
                    df['Gain'] = df['Gain'].astype(str).str.extract(r'(-?\d+(?:\.\d+)?)', expand=False).astype(float)
                    
                    # Add missing columns with default values for compatibility
                    df['Kostak'] = 'N/A'
                    df['Subject'] = 'N/A' 
                    df['Type'] = 'Mainline'  # Default type
                    
                    # Remove any rows where all values are NaN
                    df = df.dropna(how='all')
                    
                    # Print cleaned dataframe for debugging
                    print("\nCleaned DataFrame:")
                    print(df.head())
                    
                    return df
                else:
                    print(f"Unexpected number of columns: {len(df.columns)}")
                    return None
            else:
                print("No table found in the webpage")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Request error: {str(e)}")
            return None
        except Exception as e:
            print(f"Error scraping data: {str(e)}")
            return None

    @staticmethod
    def test_scraper():
        """
        Test function to verify scraper functionality
        """
        print("Testing scraper...")
        df = IPOScraper.scrape_ipo_data()
        if df is not None:
            print("\nScraper test successful!")
            print("\nDataFrame Info:")
            print(df.info())
            print("\nSample Data:")
            print(df.head())
            return True
        else:
            print("Scraper test failed!")
            return False
