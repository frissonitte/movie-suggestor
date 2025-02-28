import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('API_KEY')
access_token = os.getenv('ACCESS_TOKEN')

headers = {
    'Authorization': f'Bearer {access_token}'
}

def get_popular_movies():
    url = f'https://api.themoviedb.org/3/movie/popular?language=en-US&page=1'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_movie_details(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?language=en-US'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None