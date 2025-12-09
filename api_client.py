import requests
import os
from dotenv import load_dotenv
load_dotenv()
RAWG_URL = "https://api.rawg.io/api/games"
RAWG_KEY = os.getenv("RAWG_API_KEY")

ITAD_ID_URL = "https://api.isthereanydeal.com/games/search/v1"
ITAD_PRICE_URL = "https://api.isthereanydeal.com/games/prices/v3"
ITAD_KEY = os.getenv("ITAD_API_KEY")
class GameAPIClient:
    """
    Handles fetching game data from a public API (e.g., IsThereAnyDeal and RAWG).
    """



    def get_game_id(self, title):
        """
        Query ITAD's API for a given game's ID.
        Return game_id or None.
        """
        game_id = None
        params = {
            "key" : ITAD_KEY,
            "title": title,
            "results": 1
        }
        response = requests.get(url=ITAD_ID_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            if not data:
                print("No ITAD results")
                return None



            results = data[0]
            game_id = results["id"]
            return game_id

        else:
            print("Error getting ITAD game id.")
            return None

    def get_game_price(self, game_id, country = "US"):
        """
        Query ITAD's API for a given game's price.
        Return numeric price or None.
        """
        best_deal = float("inf") # initialize as positive infinity to be able to replace it with any sale price.
        payload = [game_id]

        headers = {
            "Content-Type": "application/json"
        }

        params = {
            "key": ITAD_KEY,
            "country": country,

        }
        response = requests.post(url=ITAD_PRICE_URL, params=params, json=payload, headers=headers)
        if response.status_code != 200:
            print("Error fetching price:", response.status_code, response.text)
            return None

        data = response.json()
        if not data:
            print("Error getting ITAD price")
            return None

        deals = data[0].get("deals",[])
        if not deals:
            return None

        for deal in deals:
            current_deal = deal["price"]["amount"]
            if current_deal < best_deal:
                best_deal = current_deal
        print(f"The best price is ${best_deal}")
        return best_deal


    def get_game_rating(self, title):
        """
        Query RAWG's API for a given game's information.
        Return game's metacritic score or None.
        """

        params = {
            "key" : RAWG_KEY,
            "search": title,
            "page_size": 1
        }
        response = requests.get(url=RAWG_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            results = data.get("results")

            if results:
                game = results[0]
                print("Name:", game["name"])
                print("Released:", game["released"])
                print("Rating:", game["rating"])
                print("Metacritic:", game.get("metacritic"))
                print("Platforms:", [p["platform"]["name"] for p in game["platforms"]])
                return game.get("metacritic")
            else:
                print("No results found.")
        else:
            print("Error:", response.status_code, response.text)

        return None
