import sqlite3
from flask import Flask, g, render_template, request, redirect, flash

app = Flask(__name__)

DATABASE = "movie.db"

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/movies", methods=["GET", "POST"])
def movies():
    movies = get_db().execute(
        "SELECT title, genres FROM movies WHERE genres LIKE '%Comedy%'"
    ).fetchall()
    
    if not movies:
        flash("No movies found", "danger") 
    
    return render_template("movies.html",movies=movies)

@app.route("/search", methods=["POST"])
def search():
    search_query = request.form.get("search_query")
    if search_query:
        db = get_db()
        movies = db.execute(
            """
            SELECT title, genres 
            FROM movies 
            JOIN tags ON movies.movieId = tags.movieId  
            WHERE title LIKE ? OR genres LIKE ? OR tag LIKE ?
            """,
            (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%")
        ).fetchall()

        if not movies:
            flash("No movies found", "danger") 

        return render_template("search_results.html", movies=movies, search_query=search_query)
    
    flash("Enter a search term.", "danger") 
          
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.run(debug=True)
