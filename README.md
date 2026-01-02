# Game Price Comparer

A Python backend application that compares video game prices between Steam (via web scraping) and IsThereAnyDeal (ITAD) API, while also fetching Metacritic ratings from RAWG. The project is evolving into a Flask-based web app with persistent storage for price history, favorites, and user accounts.

This project demonstrates API integration, web scraping, backend architecture, and database design using Python.

## Features

- Scrapes Steam for current game prices  
- Fetches price data from the IsThereAnyDeal (ITAD) API  
- Retrieves Metacritic ratings from the RAWG API  
- Compares prices and determines the cheaper source  
- Stores historical price snapshots in a database  
- Allows users to save favorite games  
- Backend built with Flask and SQLAlchemy (UI in progress)

## Demo

![Game Price Comparer Demo](assets/gifs/GamePriceShowcase.gif)

## Technologies Used

- Python 3
- Flask
- SQLAlchemy (SQLite)
- Requests
- BeautifulSoup4
- python-dotenv
- REST APIs (HTTP / JSON)
- Object-Oriented Programming (OOP)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/KeithHardyII/Game-Price-Checker.git
cd game-price-comparer
```

2. Create a `.env` file in the project root with your API keys:
```
RAWG_API_KEY=your_rawg_key
ITAD_API_KEY=your_itad_key
FLASK_KEY=your_secret_key
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage
## CLI (current)

Run the script and enter a game title:
```bash
python main.py
```

Example output:
```
Enter game title: Cyberpunk 2077
Steam's price: $29.99
ITAD's price: $24.99
ITAD (API) is cheaper by $5.00
```

Flask App (in progress)
```bash
flask run
```

The Flask app is being expanded to support:

- User authentication
- Viewing saved favorites
- Browsing historical price data

## Notes / Future Improvements

- Finish user authentication and authorization
- Add relationships between users, favorites, and price history
- Move remaining CLI logic fully into Flask routes
- Add HTML templates with Bootstrap and WTForms
- Improve error handling for edge cases (free games, missing prices, regions)

## License

This project is open-source and free to use.
