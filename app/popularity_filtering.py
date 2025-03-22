from flask import Blueprint, render_template, request, session, flash, url_for
from .models import Book, Rating, db
import pandas as pd

# Blueprint for popularity-based filtering
popularity_bp = Blueprint("popularity_bp", __name__)

# Function to fetch popular books by genre
def get_popular_books(genre=None, top_n=5):
    # Fetch books and their rating count
    books = db.session.query(
        Book.ISBN, Book.book_title, Book.book_author, Book.genre, Book.publisher, Book.year_of_publication,
        db.func.count(Rating.book_rating).label("rating_count")
    ).join(Rating, Book.ISBN == Rating.ISBN).group_by(Book.ISBN).order_by(db.desc("rating_count"))

    if genre:
        books = books.filter(Book.genre == genre)  # Filter by selected genre

    books_df = pd.DataFrame(
        books.all(),
        columns=["ISBN", "Title", "Author", "Genre", "Publisher", "Year", "rating_count"]
    )

    return books_df.head(top_n) if not books_df.empty else []

# **Route for Popularity-Based Filtering Page**
@popularity_bp.route("/popularity_based", methods=["GET"])
def popularity_based():
    if "user_id" not in session:
        flash("Please log in to access recommendations.", "warning")
        return render_template("signin.html")

    # Get selected genre from dropdown
    genre = request.args.get("genre", None)

    # Fetch all unique genres from the database
    all_genres = db.session.query(Book.genre).distinct().all()
    all_genres = [g[0] for g in all_genres if g[0]]  # Remove None values

    # Fetch popular books based on the selected genre
    popular_books = get_popular_books(genre)

    return render_template(
        "popularity_based.html",
        genres=all_genres,
        selected_genre=genre,
        popular_books=popular_books
    )
