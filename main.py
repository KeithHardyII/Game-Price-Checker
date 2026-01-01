from models import Game
from api_client import GameAPIClient
from scraper import GameScraper
from comparer import PriceComparer
import urllib.parse
import datetime
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, DateTime
import os
'''
Remove main and move functionality into flask routes
add html css bootstrap and wtforms
finish adding login logic
establish relationships between databases
'''

# Create Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
ckeditor = CKEditor(app)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

# Create Database
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///accounts.db")
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Create a User table for all registered users
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))

# Create favorite table
class Favorite(db.Model):
    __tablename__ = "favorites"
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.String(100), nullable=False)
    game_name = db.Column(db.String(255), nullable=False)
    saved_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# Create snapshot table
class Price_snapshots(db.Model):
    __tablename__ = "prices"
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.String(100), nullable=False)
    game_name = db.Column(db.String(255), nullable=False)
    api_price = db.Column(db.Float, nullable=False)
    scraped_price = db.Column(db.Float, nullable=False)
    checked_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

with app.app_context():
    db.create_all()

# TEMP: running inside app context for now
# Will move this logic into routes after auth is added
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
    store_price = Price_snapshots(game_id=game_id,game_name=game.title,api_price=game.api_price,scraped_price=game.scraped_price)
    db.session.add(store_price)
    db.session.commit()



@app.route('/')
def default():
    return "<h1>Test<h1/>"

@app.route("/user/add") # add a form and salt passwords
def add_user():
    username = request.args.get("username")
    user_password = request.args.get("user_password")

    if not username or not user_password:
        return "Missing username or user_password", 400

    new_user = User(username=username, password=user_password)
    db.session.add(new_user)
    db.session.commit()

    return f"Saved {username} as a new user"

@app.route("/user")
def list_users():
    users = User.query.all()
    return "<br>".join(f"{u.username} {u.password}" for u in users)

@app.route("/history")
def list_history():
    history = Price_snapshots.query.all()
    return "<br>".join(f"{f.game_name} ({f.game_id}) Api = {f.api_price}  Scraped = {f.scraped_price}" for f in history)

@app.route("/favorites/add")
def add_favorite():
    game_id = request.args.get("game_id")
    game_name = request.args.get("game_name")

    if not game_id or not game_name:
        return "Missing game_id or game_name", 400

    fav = Favorite(game_id=game_id, game_name=game_name)
    db.session.add(fav)
    db.session.commit()

    return f"Saved {game_name} as favorite"

@app.route("/favorites")
def list_favorites():
    favorites = Favorite.query.all()
    return "<br>".join(f"{f.game_name} ({f.game_id})" for f in favorites)

if __name__ == "__main__":
    with app.app_context(): # Temp used for testing comment out these 2 lines for flask functionality
        main()
    app.run(debug=True, port=5001)