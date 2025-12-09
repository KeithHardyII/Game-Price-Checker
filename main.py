from models import Game
from api_client import GameAPIClient
from scraper import GameScraper
from comparer import PriceComparer
import urllib.parse

def main():
    title = input("Enter game title: ")

    game = Game(title)

    # --- API price ---
    api = GameAPIClient()
    game_id = api.get_game_id(title)
    game.api_price = api.get_game_price(game_id)
    game.api_metacritic = api.get_game_rating(title)

    # --- Scraped price ---
    scraper = GameScraper()
    query = urllib.parse.quote(title) # Encode the "title" string so that it can be used in a URL
    game_url = scraper.fetch_page(f"https://store.steampowered.com/search/?term={query}")
    game.scraped_price = scraper.extract_price(game_url)

    # --- Compare ---
    comparer = PriceComparer()
    result = comparer.compare(game)
    print(f"Steam's price: ${game.scraped_price}\n"
          f"ITAD's price: ${game.api_price}\n"
          f"{result}")


if __name__ == "__main__":
    main()