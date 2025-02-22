import sqlite3
from flask import Flask, g, render_template, request, redirect, abort

app = Flask(__name__)

DATABASE = "movie.db"

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.route("/")
def index():
   return render_template("index.html")

@app.route("/movies", methods=["GET", "POST"])
def movies():
    movies = get_db().execute(
        "SELECT title, genres FROM movies WHERE genres LIKE '%Comedy%'"
    ).fetchall()
    
    if not movies:
        abort(404, description="No movies found in this genre.")
    
    return render_template("movies.html",movies=movies)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.run(debug=True)
