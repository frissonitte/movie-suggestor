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
        movie_title TEXT NOT NULL,python
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
        FOREIGN KEY (userId) REFERENCES movies (userId)
    )
''')

cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        hash TEXT NOT NULL
    )
''')


#Data insertation
movies.to_sql('movies',conn, if_exists='replace', index=False)
ratings.to_sql('ratings',conn, if_exists='replace', index=False)
links.to_sql('links', conn, if_exists='replace', index=False)
tags.to_sql('tags', conn, if_exists='replace', index=False)

conn.commit()
conn.close()

print("Database created and populated successfully!")