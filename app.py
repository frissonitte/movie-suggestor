import sqlite3
from flask import Flask, g, render_template, request, redirect, flash, session
from flask_session import Session
from auth import auth, login_required
import tmdb_api

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.register_blueprint(auth)

DATABASE = "movie.db"

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.route("/", methods=["GET", "POST"])
def index():
    popular_movies = tmdb_api.get_popular_movies()

    if popular_movies and 'results' in popular_movies:
        movies = popular_movies['results']
    else:
        movies = []
    return render_template('index.html', movies=movies)

@app.route("/watchlist", methods=["GET", "POST"])
@login_required
def watchlist():
    return render_template("watchlist.html")

@app.route("/search", methods=["POST"])
def search():
    search_query = request.form.get("search_query")
    if search_query:
        db = get_db()
        movie_ids = db.execute(
            """
            SELECT DISTINCT tmdbId
            FROM links 
            JOIN movies ON links.movieId = movies.movieId 
            JOIN tags ON movies.movieId = tags.movieId  
            WHERE title LIKE ? OR genres LIKE ? OR tag LIKE ?
            """,
            (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%")
        ).fetchall()

        if not movie_ids:
            flash("No movies found", "danger")
            return redirect("/")

        movies = []
        for tmdb_id in movie_ids:
            movie_details = tmdb_api.get_movie_details(tmdb_id[0])
            if movie_details:
                movies.append(movie_details)
        
        return render_template("search_results.html", movies=movies, search_query=search_query)
    
    flash("Enter a search term.", "danger")
    return redirect("/")

@app.route('/movie/<int:movie_id>') 
def movie_details(movie_id):
    movie = tmdb_api.get_movie_details(movie_id)
    if movie:
        return render_template('movie_details.html', movie=movie)
    else:
        return "No movies found!", 404

          
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.run(debug=True)
