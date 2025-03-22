from flask import Blueprint, render_template, request, session, flash
from .models import Book, Rating, Users, db
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Blueprint for content-based filtering
content_bp = Blueprint("content_bp", __name__)

# Function to generate recommendations
def get_recommendations(user_id, genre=None, top_n=5):
    books = Book.query.all()
    ratings = Rating.query.all()

    books_df = pd.DataFrame(
        [(b.ISBN, b.book_title, b.book_author, b.publisher, b.genre, b.year_of_publication) for b in books],
        columns=["ISBN", "Title", "Author", "Publisher", "Genre", "Year"],
    )

    ratings_df = pd.DataFrame(
        [(r.user_id, r.ISBN) for r in ratings], columns=["User_ID", "ISBN"]
    )

    if books_df.empty:
        return []

    books_df["book_profile"] = books_df.apply(
        lambda x: f"{x['Title']} {x['Author']} {x['Publisher']} {x['Genre']}", axis=1
    )

    tfidf_vectorizer = TfidfVectorizer(max_features=5000)
    tfidf_books = tfidf_vectorizer.fit_transform(books_df["book_profile"])

    if ratings_df.empty:
        return books_df.sample(n=min(top_n, len(books_df)))[["ISBN", "Title", "Author", "Genre"]]

    if genre:
        books_df = books_df[books_df["Genre"].str.lower() == genre.lower()]

    return books_df.head(top_n) if len(books_df) >= top_n else books_df

# Route for Content-Based Filtering Page
@content_bp.route("/content_based", methods=["GET"])
def content_based():
    if "user_id" not in session:
        flash("Please log in to access recommendations.", "warning")
        return render_template("signin.html")

    user_id = session["user_id"]
    genre = request.args.get("genre", None)

    recommendations = get_recommendations(user_id, genre, top_n=5)

    all_genres = db.session.query(Book.genre).distinct().all()
    all_genres = [g[0] for g in all_genres if g[0]]

    return render_template("content_based.html", recommendations=recommendations, genres=all_genres, selected_genre=genre)

# ✅ New Route to View Book Details
@content_bp.route("/book/<isbn>", methods=["GET", "POST"])
def view_book(isbn):
    if "user_id" not in session:
        flash("⚠️ Please log in to view book details.", "warning")
        return redirect(url_for("auth_bp.signin"))  # Redirect to login page

    user_id = session["user_id"]
    book = Book.query.filter_by(ISBN=isbn).first()

    if not book:
        flash("⚠️ The requested book does not exist in our database!", "danger")
        return redirect(url_for("content_bp.content_based"))

    # Fetch all ratings for this book
    ratings = Rating.query.filter_by(ISBN=isbn).all()

    # Calculate total ratings
    total_ratings = len(ratings)

    # Count occurrences of each rating (1-10)
    rating_data = {}
    for rating in ratings:
        if rating.book_rating:  # Ensure book_rating is not None
            rating_data[rating.book_rating] = rating_data.get(rating.book_rating, 0) + 1

    # Check if the current user has already rated this book
    user_rating = Rating.query.filter_by(user_id=user_id, ISBN=isbn).first()

    # Handle form submission (if user submits a rating)
    if request.method == "POST":
        new_rating = int(request.form.get("rating"))

        if user_rating:
            # Update existing rating
            user_rating.book_rating = new_rating
            flash("✅ Your rating has been updated!", "success")
        else:
            # Add new rating
            new_rating_entry = Rating(user_id=user_id, ISBN=isbn, book_rating=new_rating)
            db.session.add(new_rating_entry)
            flash("✅ Your rating has been submitted!", "success")

        db.session.commit()
        return redirect(url_for("content_bp.view_book", isbn=isbn))  # Refresh page

    return render_template(
        "book_details.html",
        book=book,
        rating_data=rating_data,
        total_ratings=total_ratings,
        user_rating=user_rating,
    )


