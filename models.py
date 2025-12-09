class Game:
    """
    Represents a game with basic info: title, API price, scraped price, etc.
    """
    def __init__(self, title, api_metacritic=None, scraped_price=None, api_price=None):
        self.title = title
        self.api_price = api_price
        self.api_metacritic = api_metacritic
        self.scraped_price = scraped_price

    def __repr__(self):
        return f"<Game {self.title} | Metacritic: {self.api_metacritic} | Web: {self.scraped_price} | API: {self.api_price}>"
