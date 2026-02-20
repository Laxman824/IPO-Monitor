# # utils/scraper.py
# import requests
# import pandas as pd
# from bs4 import BeautifulSoup
# from io import StringIO
# import time
# from config.config import Config

# class IPOScraper:
#     @staticmethod
#     def scrape_ipo_data():
#         try:
#             # Add headers to mimic a browser request
#             headers = {
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#             }
            
#             # Make the request with headers
#             response = requests.get(Config.IPO_URL, headers=headers, timeout=10)
#             response.raise_for_status()  # Raise an error for bad status codes
            
#             # Print response status and first few characters for debugging
#             print(f"Response status: {response.status_code}")
#             print(f"Response preview: {response.text[:200]}")
            
#             soup = BeautifulSoup(response.text, 'html.parser')
            
#             # Try to find table with more specific selectors
#             table = soup.find('table', {'class': ['wp-block-table', 'table']})
#             if not table:
#                 print("Trying alternative table finding methods...")
#                 tables = soup.find_all('table')
#                 if tables:
#                     table = tables[0]  # Get the first table if multiple exist
                
#             if table:
#                 # Convert table to string and wrap with StringIO
#                 table_str = StringIO(str(table))
                
#                 try:
#                     # Try parsing with different parsers
#                     df = pd.read_html(table_str, flavor='bs4')[0]
#                 except Exception as e:
#                     print(f"First parsing attempt failed: {e}")
#                     try:
#                         df = pd.read_html(str(table), flavor='html5lib')[0]
#                     except Exception as e2:
#                         print(f"Second parsing attempt failed: {e2}")
#                         return None
                
#                 # Print raw dataframe for debugging
#                 print("Raw DataFrame:")
#                 print(df.head())
                
#                 # Clean and standardize column names
#                 # Updated to match current website structure
#                 expected_columns = ['Current IPOs', 'IPO GMP', 'IPO Price', 'Gain', 'Date']
                
#                 if len(df.columns) >= len(expected_columns):
#                     df.columns = expected_columns
                    
#                     # Data cleaning for new format
#                     df['Gain'] = df['Gain'].astype(str).str.extract(r'(-?\d+(?:\.\d+)?)', expand=False).astype(float)
                    
#                     # Add missing columns with default values for compatibility
#                     df['Kostak'] = 'N/A'
#                     df['Subject'] = 'N/A' 
#                     df['Type'] = 'Mainline'  # Default type
                    
#                     # Remove any rows where all values are NaN
#                     df = df.dropna(how='all')
                    
#                     # Print cleaned dataframe for debugging
#                     print("\nCleaned DataFrame:")
#                     print(df.head())
                    
#                     return df
#                 else:
#                     print(f"Unexpected number of columns: {len(df.columns)}")
#                     return None
#             else:
#                 print("No table found in the webpage")
#                 return None
                
#         except requests.exceptions.RequestException as e:
#             print(f"Request error: {str(e)}")
#             return None
#         except Exception as e:
#             print(f"Error scraping data: {str(e)}")
#             return None

#     @staticmethod
#     def test_scraper():
#         """
#         Test function to verify scraper functionality
#         """
#         print("Testing scraper...")
#         df = IPOScraper.scrape_ipo_data()
#         if df is not None:
#             print("\nScraper test successful!")
#             print("\nDataFrame Info:")
#             print(df.info())
#             print("\nSample Data:")
#             print(df.head())
#             return True
#         else:
#             print("Scraper test failed!")
#             return False
# utils/scraper.py


# import cloudscraper
# import requests
# import pandas as pd
# from bs4 import BeautifulSoup
# from io import StringIO
# import time
# import random
# import logging
# from typing import Optional
# from config.config import Config

# logger = logging.getLogger(__name__)


# class IPOScraper:
#     """Robust IPO GMP data scraper with retry logic and fallbacks."""

#     def __init__(self):
#         self.config = Config.get()
#         import cloudscraper
#         self.session = cloudscraper.create_scraper()
#         # self.session = requests.Session()
#         self.session.headers.update({
#             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#             "Accept-Language": "en-US,en;q=0.9",
#             "Accept-Encoding": "gzip, deflate, br",
#             "Connection": "keep-alive",
#             "Upgrade-Insecure-Requests": "1",
#         })

#     def _get_random_ua(self) -> str:
#         return random.choice(self.config.USER_AGENTS)

#     def _fetch_page(self, url: str, attempt: int = 1) -> Optional[str]:
#         """Fetch a page with retry + exponential backoff."""
#         max_retries = self.config.MAX_RETRIES
#         delay = self.config.RETRY_DELAY

#         for i in range(max_retries):
#             try:
#                 self.session.headers["User-Agent"] = self._get_random_ua()
#                 response = self.session.get(
#                     url, timeout=self.config.REQUEST_TIMEOUT
#                 )
#                 response.raise_for_status()
#                 logger.info(f"✅ Fetched {url} (status {response.status_code})")
#                 return response.text

#             except requests.exceptions.Timeout:
#                 logger.warning(f"⏱️ Timeout on attempt {i+1}/{max_retries} for {url}")
#             except requests.exceptions.ConnectionError:
#                 logger.warning(f"🔌 Connection error attempt {i+1}/{max_retries}")
#             except requests.exceptions.HTTPError as e:
#                 logger.warning(f"🚫 HTTP {e.response.status_code} on attempt {i+1}")
#                 if e.response.status_code == 403:
#                     delay *= 2  # back off harder on 403
#             except Exception as e:
#                 logger.error(f"❌ Unexpected error: {e}")

#             if i < max_retries - 1:
#                 sleep_time = delay * (2 ** i) + random.uniform(0, 1)
#                 logger.info(f"💤 Sleeping {sleep_time:.1f}s before retry…")
#                 time.sleep(sleep_time)

#         return None

#     def _parse_table(self, html: str) -> Optional[pd.DataFrame]:
#         """Extract and parse the IPO table from HTML."""
#         soup = BeautifulSoup(html, "html.parser")
#         table = None

#         # Strategy 1: specific table ID for current GMP data
#                 # Look for ANY table that contains typical IPO headers
#         for t in soup.find_all("table"):
#             header_text = t.get_text().lower()
#             if "ipo" in header_text and "gmp" in header_text and "price" in header_text:
#                 table = t
#                 break
#         # table = soup.find("table", {"id": "tablepress-21"})
        
#         # Strategy 2: look for table with GMP in header
#         if not table:
#             for t in soup.find_all("table"):
#                 headers = t.find_all(["th", "td"])
#                 header_text = " ".join([h.get_text().strip() for h in headers[:10]])
#                 if "GMP" in header_text and "IPO" in header_text:
#                     table = t
#                     break

#         # Strategy 3: first table with enough rows
#         if not table:
#             for t in soup.find_all("table"):
#                 rows = t.find_all("tr")
#                 if len(rows) >= 3:
#                     table = t
#                     break

#         if not table:
#             logger.error("No suitable table found in HTML")
#             return None

#         # Parse table
#         for parser in ["bs4", "html5lib", "lxml"]:
#             try:
#                 dfs = pd.read_html(StringIO(str(table)), flavor=parser)
#                 if dfs and len(dfs[0]) > 0:
#                     logger.info(f"✅ Parsed table with '{parser}' parser")
#                     return dfs[0]
#             except Exception as e:
#                 logger.debug(f"Parser '{parser}' failed: {e}")
#                 continue

#         return None

#     def _clean_dataframe(self, df: pd.DataFrame) -> Optional[pd.DataFrame]:
#         """Clean and standardize the scraped dataframe."""
#         if df is None or df.empty:
#             return None

#         # Drop fully-empty rows/cols
#         df = df.dropna(how="all").dropna(axis=1, how="all")

#         # Reset if header got absorbed into data
#         if df.shape[1] < 3:
#             logger.error(f"Too few columns ({df.shape[1]})")
#             return None

#         # Standardize column names
#         col_mapping = {
#             0: "Current IPOs",
#             1: "IPO GMP", 
#             2: "IPO Price",
#             3: "Gain",
#             4: "Date",
#         }

#         if len(df.columns) >= 5:
#             df.columns = [col_mapping.get(i, f"col_{i}") for i in range(len(df.columns))]
#         elif len(df.columns) == 4:
#             df.columns = ["Current IPOs", "IPO GMP", "Gain", "Date"]
#         elif len(df.columns) == 3:
#             df.columns = ["Current IPOs", "Gain", "Date"]
#         else:
#             logger.error(f"Unexpected column count: {len(df.columns)}")
#             return None

#         # Parse Gain column
#         if "Gain" in df.columns:
#             df["Gain"] = (
#                 df["Gain"]
#                 .astype(str)
#                 .str.replace("%", "", regex=False)
#                 .str.replace("+", "", regex=False)
#                 .str.extract(r"(-?\d+(?:\.\d+)?)", expand=False)
#             )
#             df["Gain"] = pd.to_numeric(df["Gain"], errors="coerce").fillna(0)

#         # Parse IPO GMP
#         if "IPO GMP" in df.columns:
#             df["IPO GMP"] = (
#                 df["IPO GMP"]
#                 .astype(str)
#                 .str.extract(r"(-?\d+(?:\.\d+)?)", expand=False)
#             )
#             df["IPO GMP"] = pd.to_numeric(df["IPO GMP"], errors="coerce").fillna(0)

#         # Parse IPO Price
#         if "IPO Price" in df.columns:
#             df["IPO Price"] = (
#                 df["IPO Price"]
#                 .astype(str)
#                 .str.replace("₹", "", regex=False)
#                 .str.replace(",", "", regex=False)
#                 .str.extract(r"(\d+(?:\.\d+)?)", expand=False)
#             )
#             df["IPO Price"] = pd.to_numeric(df["IPO Price"], errors="coerce").fillna(0)

#         # Add missing columns
#         if "Type" not in df.columns:
#             df["Type"] = df["Current IPOs"].apply(
#                 lambda x: "SME" if "sme" in str(x).lower() else "Mainline"
#             )
#         if "Kostak" not in df.columns:
#             df["Kostak"] = "N/A"
#         if "Subject" not in df.columns:
#             df["Subject"] = "N/A"

#         # Clean IPO names
#         df["Current IPOs"] = (
#             df["Current IPOs"]
#             .astype(str)
#             .str.strip()
#             .str.replace(r"\s+", " ", regex=True)
#         )

#         # Remove junk rows
#         df = df[
#             ~df["Current IPOs"].str.contains(
#                 "current|ipo name|company", case=False, na=False
#             )
#         ]
#         df = df[df["Current IPOs"].str.len() > 2]

#         df = df.reset_index(drop=True)
#         logger.info(f"✅ Cleaned dataframe: {len(df)} IPOs")
#         return df

#     def scrape_ipo_data(self) -> Optional[pd.DataFrame]:
#         """Main entry: scrape, parse, clean, return DataFrame."""
#         urls = [self.config.IPO_URL] + [
#             u for u in self.config.FALLBACK_URLS if u != self.config.IPO_URL
#         ]

#         for url in urls:
#             logger.info(f"🔍 Trying {url}")
#             html = self._fetch_page(url)
#             if not html:
#                 continue

#             raw_df = self._parse_table(html)
#             if raw_df is None:
#                 continue

#             clean_df = self._clean_dataframe(raw_df)
#             if clean_df is not None and not clean_df.empty:
#                 return clean_df

#         logger.error("❌ All sources failed")
#         return None

#     @staticmethod
#     def test_scraper():
#         """Test function to verify scraper functionality."""
#         print("=" * 50)
#         print("Testing IPO Scraper…")
#         print("=" * 50)

#         scraper = IPOScraper()
#         df = scraper.scrape_ipo_data()

#         if df is not None:
#             print(f"\n✅ SUCCESS — {len(df)} IPOs found")
#             print(f"\nColumns: {list(df.columns)}")
#             print(f"\nSample:\n{df.head()}")
#             print(f"\nGain range: {df['Gain'].min():.1f}% to {df['Gain'].max():.1f}%")
#             return True
#         else:
#             print("\n❌ FAILED — No data returned")
#             return False


# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)
#     IPOScraper.test_scraper()


# # utils/scraper.py
# import requests
# import urllib.request
# import pandas as pd
# from bs4 import BeautifulSoup
# from io import StringIO
# import time
# import logging
# from typing import Optional, List
# from config.config import Config

# logger = logging.getLogger(__name__)

# class IPOScraper:
#     """Robust IPO GMP data scraper that tests all tables dynamically."""

#     def __init__(self):
#         try:
#             self.config = Config.get() if hasattr(Config, "get") else Config
#         except Exception:
#             self.config = Config

#         self.session = requests.Session()
        
#         # Using the exact User-Agent that worked in your successful logs
#         self.session.headers.update(
#             {
#                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#                 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#                 "Accept-Language": "en-US,en;q=0.9",
#                 "Connection": "keep-alive",
#             }
#         )

#     def _fetch_page(self, url: str) -> Optional:
#         """Fetch a page with retry logic and a fallback fetcher."""
#         max_retries = getattr(self.config, "MAX_RETRIES", 3)
#         base_delay = getattr(self.config, "RETRY_DELAY", 2)
#         timeout = getattr(self.config, "REQUEST_TIMEOUT", 15)

#         for attempt in range(max_retries):
#             try:
#                 response = self.session.get(url, timeout=timeout)
#                 response.raise_for_status()
#                 return response.text
#             except Exception as e:
#                 logger.warning(f"⚠️ Request attempt {attempt + 1} failed: {e}")
#                 if attempt < max_retries - 1:
#                     time.sleep(base_delay * (2 ** attempt))

#         # Fallback: Try standard urllib if requests is completely blocked
#         try:
#             req = urllib.request.Request(url, headers=self.session.headers)
#             with urllib.request.urlopen(req, timeout=timeout) as response:
#                 return response.read().decode('utf-8')
#         except Exception as e:
#             logger.error(f"❌ Urllib fallback failed for {url}: {e}")
            
#         return None

#     def _parse_all_tables(self, html: str) -> List:
#         """Extract and parse ALL tables from the HTML."""
#         soup = BeautifulSoup(html, "html.parser")
#         candidates = soup.find_all("table")
        
#         dfs =[]
#         for table in candidates:
#             # We skip tiny tables (like calendars or small widgets)
#             if len(table.find_all("tr")) < 3:
#                 continue
                
#             for parser in:
#                 try:
#                     parsed = pd.read_html(StringIO(str(table)), flavor=parser)
#                     if parsed and len(parsed) > 0:
#                         dfs.append(parsed)
#                         break  # Found successfully, move to next table
#                 except Exception:
#                     continue
#         return dfs

#     def _clean_dataframe(self, df: pd.DataFrame) -> Optional:
#         """Dynamically map and clean the dataframe regardless of column order."""
#         if df is None or df.empty:
#             return None

#         # Sometimes pandas parses the headers as the first data row. Fix that:
#         if str(df.columns).isdigit():
#             df.columns = df.iloc
#             df = df.reset_index(drop=True)

#         df = df.dropna(how="all").dropna(axis=1, how="all")

#         # Verify this table actually has IPO-related data to avoid menu tables
#         text_content = df.astype(str).to_string().lower()
#         if "gmp" not in text_content and "ipo" not in text_content and "price" not in text_content:
#             return None

#         str_cols =
#         mapped_df = pd.DataFrame()

#         # 1. Map Current IPOs
#         for c, sc in zip(df.columns, str_cols):
#             if "ipo" in sc or "company" in sc or "name" in sc:
#                 mapped_df = df
#                 break
                
#         # 2. Map IPO GMP
#         for c, sc in zip(df.columns, str_cols):
#             if "gmp" in sc and "ipo" not in sc:
#                 mapped_df = df
#                 break
#         if "IPO GMP" not in mapped_df.columns:
#             for c, sc in zip(df.columns, str_cols):
#                 if "gmp" in sc:
#                     mapped_df = df
#                     break

#         # 3. Map IPO Price
#         for c, sc in zip(df.columns, str_cols):
#             if "price" in sc or "band" in sc:
#                 mapped_df = df
#                 break

#         # 4. Map Gain
#         for c, sc in zip(df.columns, str_cols):
#             if "gain" in sc or "est" in sc or "%" in sc:
#                 mapped_df = df
#                 break

#         # 5. Map Date
#         for c, sc in zip(df.columns, str_cols):
#             if "date" in sc or "open" in sc or "close" in sc:
#                 mapped_df = df
#                 break

#         # If dynamic mapping failed, fallback to positional mapping
#         if "Current IPOs" not in mapped_df.columns or "Gain" not in mapped_df.columns:
#             mapped_df = pd.DataFrame()
#             if len(df.columns) >= 5:
#                 mapped_df = df.iloc
#                 mapped_df = df.iloc
#                 mapped_df = df.iloc
#                 mapped_df = df.iloc
#                 mapped_df = df.iloc
#             else:
#                 return None

#         # Ensure all columns exist to prevent Streamlit UI errors
#         for col in:
#             if col not in mapped_df.columns:
#                 mapped_df = "N/A"

#         # Clean Gain column for calculations (e.g. "6.17%" -> 6.17)
#         mapped_df = (
#             mapped_df
#             .astype(str)
#             .str.replace("%", "", regex=False)
#             .str.replace("+", "", regex=False)
#             .str.extract(r"(-?\d+(?:\.\d+)?)", expand=False)
#         )
#         mapped_df = pd.to_numeric(mapped_df, errors="coerce").fillna(0.0)

#         # Clean IPO GMP and IPO Price safely (retain "₹" formats for display if desired, or ensure string)
#         mapped_df = mapped_df.astype(str).replace("nan", "N/A")
#         mapped_df = mapped_df.astype(str).replace("nan", "N/A")

#         # Add missing defaults
#         mapped_df = mapped_df.apply(
#             lambda x: "SME" if "sme" in str(x).lower() else "Mainline"
#         )
#         mapped_df = "N/A"
#         mapped_df = "N/A"

#         # Clean IPO names
#         mapped_df = mapped_df.astype(str).str.strip().str.replace(r"\s+", " ", regex=True)

#         # Remove header/junk rows
#         mapped_df = mapped_df[
#             ~mapped_df.str.contains(r"^(IPO|Company|Current|Name|Sr)", case=False, na=False)
#         ]
#         mapped_df = mapped_df.str.len() > 2]

#         return mapped_df.reset_index(drop=True)

#     def scrape_ipo_data(self) -> Optional:
#         """Main entry: scrape, parse, clean, return DataFrame."""
#         urls =[]
#         if hasattr(self.config, "IPO_URL") and self.config.IPO_URL:
#             urls.append(self.config.IPO_URL)
#         if hasattr(self.config, "FALLBACK_URLS"):
#             urls.extend()
            
#         if not urls:
#             urls =

#         for url in urls:
#             logger.info(f"🔍 Trying {url}")
#             html = self._fetch_page(url)
#             if not html:
#                 continue

#             raw_dfs = self._parse_all_tables(html)
            
#             # Test every table on the page until one succeeds
#             for raw_df in raw_dfs:
#                 clean_df = self._clean_dataframe(raw_df)
#                 # If it cleaned successfully and has at least a couple of rows of real data
#                 if clean_df is not None and not clean_df.empty and len(clean_df) >= 2:
#                     logger.info(f"✅ Successfully scraped {len(clean_df)} IPOs from {url}")
#                     return clean_df

#         logger.error("❌ All sources and tables failed")
#         return None

#     @staticmethod
#     def test_scraper():
#         print("=" * 60)
#         print("  IPO Scraper — Test Suite")
#         print("=" * 60)

#         scraper = IPOScraper()
#         df = scraper.scrape_ipo_data()

#         if df is not None and not df.empty:
#             print(f"\n✅ SUCCESS — {len(df)} IPOs found")
#             print(f"\n📋 Columns : {list(df.columns)}")
#             print(f"📊 Gain    : {df.min():.1f}% → {df.max():.1f}%")
#             print(f"\n🔍 Sample Data:")
#             print(df.head().to_string(index=False))
#             print("\n" + "=" * 60)
#             return True
#         else:
#             print("\n❌ FAILED — No data returned")
#             print("   Check your network connection or source URLs")
#             print("\n" + "=" * 60)
#             return False

# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s  %(message)s", datefmt="%H:%M:%S")
#     IPOScraper.test_scraper()


# utils/scraper.py
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import time
import logging
import random
import re
import urllib.request
from typing import Optional

# Setup logger
logger = logging.getLogger(__name__)

class IPOScraper:
    """
    Robust IPO Scraper v3.0
    - Multiple fetching methods (Requests -> Urllib)
    - Smart Table Detection (Keywords -> Size)
    - Hybrid Column Mapping (Header Name -> Index Position)
    """

    # ── Configuration ────────────────────────────────────────────────
    BASE_URL = "https://ipowatch.in/ipo-grey-market-premium-latest-ipo-gmp/"
    
    # List of User-Agents to rotate if one gets blocked
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
    ]

    def __init__(self):
        self.session = requests.Session()

    def _get_headers(self):
        return {
            'User-Agent': random.choice(self.USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

    # ── Level 1: Robust Fetching ─────────────────────────────────────
    def _fetch_html(self, url: str) -> Optional[str]:
        """Tries to fetch HTML using Requests, then falls back to Urllib."""
        
        # Method A: Requests with Session
        try:
            response = self.session.get(url, headers=self._get_headers(), timeout=15)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.warning(f"⚠️ 'Requests' failed: {e}. Switching to fallback...")

        # Method B: Urllib (Often bypasses different types of blocks)
        try:
            req = urllib.request.Request(url, headers=self._get_headers())
            with urllib.request.urlopen(req, timeout=15) as response:
                return response.read().decode('utf-8')
        except Exception as e:
            logger.error(f"❌ All fetch methods failed: {e}")
            return None

    # ── Level 2: Smart Table Parsing ─────────────────────────────────
    def _find_correct_table(self, soup: BeautifulSoup) -> Optional[pd.DataFrame]:
        """
        Scans ALL tables on page.
        1. Checks if table contains 'GMP' or 'IPO'.
        2. If not found, falls back to the first table with > 3 rows.
        """
        tables = soup.find_all('table')
        
        if not tables:
            return None

        # Strategy 1: Content-based matching (The "Smart" way)
        for table in tables:
            text = table.get_text().lower()
            # If the table talks about GMP and IPOs, it's the one we want
            if 'gmp' in text and 'ipo' in text:
                try:
                    df = pd.read_html(StringIO(str(table)))[0]
                    if len(df) > 1:
                        return df
                except:
                    continue

        # Strategy 2: Size-based matching (The "Simple/Fallback" way)
        # Just grab the first table that actually has data
        for table in tables:
            try:
                df = pd.read_html(StringIO(str(table)))[0]
                if len(df) >= 3: # Must have at least 3 rows
                    logger.info("Using fallback table (size-based detection)")
                    return df
            except:
                continue
                
        return None

    # ── Level 3: Data Cleaning & Normalization ───────────────────────
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardizes columns and data types.
        """
        # 1. Normalize Column Names
        # If we have at least 5 columns, we force our standard names
        # This fixes issues where the site changes "IPO Name" to "Company Name"
        if len(df.columns) >= 5:
            # Drop extra columns if any (site sometimes adds 'Rating' columns)
            df = df.iloc[:, :5]
            df.columns = ['Current IPOs', 'IPO GMP', 'IPO Price', 'Gain', 'Date']
        else:
            # Emergency mapping for weird tables
            logger.warning(f"Table has unexpected columns: {len(df.columns)}")
            return df

        # 2. Clean 'Gain' (Remove %, +, convert to float)
        # Extracts "-5.5" from " -5.50%" or "5%"
        df['Gain'] = df['Gain'].astype(str).str.extract(r'(-?\d+(?:\.\d+)?)', expand=False)
        df['Gain'] = pd.to_numeric(df['Gain'], errors='coerce').fillna(0)

        # 3. Clean 'IPO GMP' (Remove ₹, commas)
        df['IPO GMP'] = df['IPO GMP'].astype(str).str.replace(r'[^\d.-]', '', regex=True)
        df['IPO GMP'] = pd.to_numeric(df['IPO GMP'], errors='coerce').fillna(0)

        # 4. Clean 'IPO Price'
        df['IPO Price'] = df['IPO Price'].astype(str).str.replace(r'[^\d.]', '', regex=True)
        df['IPO Price'] = pd.to_numeric(df['IPO Price'], errors='coerce').fillna(0)

        # 5. Add Application Metadata
        # Detect SME vs Mainline based on the text
        df['Type'] = df['Current IPOs'].apply(lambda x: 'SME' if 'SME' in str(x).upper() else 'Mainline')
        df['Kostak'] = 'N/A'
        df['Subject'] = 'N/A'

        # 6. Final Filter
        # Remove header rows that got scraped as data (e.g. rows containing "IPO Name")
        df = df[~df['Current IPOs'].astype(str).str.contains('IPO|Current', case=False, na=False)]
        df = df.dropna(subset=['Current IPOs'])
        
        return df

    # ── Main Entry Point ─────────────────────────────────────────────
    def scrape_ipo_data(self):
        try:
            logger.info(f"Connecting to {self.BASE_URL}...")
            
            # Step 1: Get HTML
            html = self._fetch_html(self.BASE_URL)
            if not html:
                return None

            # Step 2: Parse Tables
            soup = BeautifulSoup(html, 'html.parser')
            raw_df = self._find_correct_table(soup)
            
            if raw_df is None or raw_df.empty:
                logger.error("No suitable IPO table found on the page.")
                return None

            # Step 3: Clean Data
            clean_df = self._clean_data(raw_df)
            
            logger.info(f"✅ Success! Scraped {len(clean_df)} IPOs.")
            return clean_df

        except Exception as e:
            logger.error(f"❌ Scraper Critical Error: {str(e)}")
            return None

    @staticmethod
    def test_scraper():
        """Run this to verify the scraper works."""
        logging.basicConfig(level=logging.INFO)
        scraper = IPOScraper()
        df = scraper.scrape_ipo_data()
        
        if df is not None:
            print("\n" + "="*50)
            print(f"🎉 SUCCESS! Found {len(df)} records")
            print("="*50)
            print(df.head().to_string())
            print("="*50)
            return True
        else:
            print("\n❌ FAILED. Check logs above.")
            return False

if __name__ == "__main__":
    IPOScraper.test_scraper()