# Записываеь в файл лучшие фильмы
import requests
import json

api_key = 'ae6b2432c1d3e9a73d69cb0e52cd66b9'
params = {
    'api_key': api_key,
    'language': 'ru-RU'
}
url = 'https://api.themoviedb.org/3/movie/popular'
response = requests.get(url, params=params)
data = response.json()
movies = [{'name': movie['title'], 'overview': movie['overview'], 'release_date': movie['release_date'],
           'vote_average': movie['vote_average']} for movie in data['results']]
with open('movies.json', 'w', encoding='utf-8') as f:
    json.dump(movies, f, ensure_ascii=False)
