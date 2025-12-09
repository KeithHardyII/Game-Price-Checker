import requests
from bs4 import BeautifulSoup

class GameScraper:
    """
    Scrapes game price from Steam's store page.
    """

    def fetch_page(self, url):
        """
        Download page HTML.
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("Failed to fetch search page")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # The first game link
        result = soup.find("a", class_="search_result_row")
        if result:
            print(f"{result.getText().split('  ')[0].strip()} found")
            return result['href']
        else:
            print("game not found")
            return None

    def extract_price(self, html):
        """
        Parse the HTML and extract the price.
        You must fill in the CSS selectors based on your chosen store.
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }

        # cookies added to bypass steam's age gate
        cookies = {
            "mature_content": "1",
            "wants_mature_content": "1",
            "birthtime": "568022401",  # a timestamp representing a birthdate in 1987
            "lastagecheckage": "1-January-1987"
        }


        response = requests.get(html, headers=headers, cookies=cookies)
        if response.status_code != 200:
            print("Failed to fetch search page")
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        final_price = None
        price = soup.find("div", class_="game_purchase_price")
        if price:
            final_price = float(price.text.strip().replace("$","").split()[0])

        sale_price = soup.find("div", class_="discount_final_price")
        if sale_price:
            final_price = float(sale_price.text.strip().replace("$","").split()[0])

        return final_price



        return None  # placeholder
