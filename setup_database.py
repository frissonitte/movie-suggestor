import sqlite3
import pandas as pd

#Loading dataset
movies = pd.read_csv('data/movies.csv')
ratings = pd.read_csv('data/ratings.csv')
links = pd.read_csv('data/links.csv')
tags = pd.read_csv('data/tags.csv')

#Creating SQL database
conn = sqlite3.connect('movie.db')
cursor = conn.cursor()

#Creating database tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS movies (
        movieId INTEGER PRIMARY KEY,
        movie_title TEXT NOT NULL,
        genres TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS ratings (
        userId INTEGER,
        movieId INTEGER,
        rating REAL,
        timestamp INTEGER,
        FOREIGN KEY (movieId) REFERENCES movies (movieId)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS links (
        movieId INTEGER,
        imdbId INTEGER,
        tmdbId INTEGER,
        FOREIGN KEY (movieId) REFERENCES movies (movieId)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS tags (
        movieId INTEGER,
        userId INTEGER,
        tag TEXT NOT NULL,
        timestamp INTEGER,
        FOREIGN KEY (movieId) REFERENCES movies (movieId)
        FOREIGN KEY (userId) REFERENCES users (id)
    )
''')

cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        hash TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS watchlist (
        movieId INTEGER,
        userId INTEGER,
        FOREIGN KEY (movieId) REFERENCES movies (movieId),
        FOREIGN KEY (userId) REFERENCES users (id),
        PRIMARY KEY (movieId, userId)
    )
''')

cursor.execute('''
    CREATE TABLE user_mapping (
        movielens_userId INTEGER PRIMARY KEY,
        system_userId INTEGER UNIQUE,
        FOREIGN KEY (system_userId) REFERENCES users(id)
    )
''')

#Data insertion
movies.to_sql('movies',conn, if_exists='replace', index=False)
ratings.to_sql('ratings',conn, if_exists='replace', index=False)
links.to_sql('links', conn, if_exists='replace', index=False)
tags.to_sql('tags', conn, if_exists='replace', index=False)

def load_movielens_users():
    conn = sqlite3.connect("movie.db")
    db = conn.cursor()

    db.execute("SELECT DISTINCT userId FROM ratings")
    movielens_users = db.fetchall()

    for user in movielens_users:
        user_id = user[0]
        
        db.execute("INSERT OR IGNORE INTO users (id, username, hash) VALUES (?, ?, ?)",
                   (user_id, f"anonymous_{user_id}", ""))
        
        db.execute("INSERT OR IGNORE INTO user_mapping (movielens_userId, system_userId) VALUES (?, ?)",
                   (user_id, user_id))
    
    conn.commit()
    conn.close()

load_movielens_users()
