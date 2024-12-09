# test_scraper.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.scraper import IPOScraper

def main():
    print("Starting scraper test...")
    IPOScraper.test_scraper()

if __name__ == "__main__":
    main()
