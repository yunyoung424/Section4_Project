import requests
import sqlite3
import json
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv('tmdb_api.env')

TMDB_API_KEY = os.getenv('TMDB_API_KEY')


# # 데이터베이스 연결
# conn = sqlite3.connect('movies.db') #db가 없는 경우 새로 생성
# cur = conn.cursor()

# # movie 테이블 생성
# cur.execute("""
#     CREATE TABLE IF NOT EXISTS movies(
#     movie_id INTEGER PRIMARY KEY,
#     title TEXT,
#     release_date TEXT,
#     popularity Float,
#     vote_average Float,
#     vote_count INTEGER,
#     overview TEXT,
#     poster_path TEXT,
#     genres TEXT
#     )""")

# # 장르 정보 사전 생성
# genre_details = {}

# # 장르 세부 정보 조회
# def get_genre_details(genre_id):
#     if genre_id in genre_details:
#         return genre_details[genre_id]

#     url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}&language=en-US"
#     response = requests.get(url)
#     genres = response.json()

#     for genre in genres['genres']:
#         genre_details[genre['id']] = genre

#     return genre_details.get(genre_id)


# # api로 데이터 가져오기
# def get_movie_data(page):
#     request_url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page={page}"
#     response = requests.get(request_url)
#     movies = response.json()

#     movie_data = []
#     for movie in movies['results']:
#         if movie.get('release_date', ''):
#             movie_id = movie['id']

#             # 장르 정보 가져오기
#             genre_ids = movie['genre_ids']
#             genres = []
#             for genre_id in genre_ids:
#                 genre_details = get_genre_details(genre_id)
#                 if genre_details:
#                     genres.append(genre_details)

#             data = {
#                 'movie_id': movie_id,
#                 'title': movie['title'],
#                 'release_date': movie['release_date'],
#                 'popularity': movie['popularity'],
#                 'vote_average': movie['vote_average'],
#                 'vote_count': movie['vote_count'],
#                 'overview': movie['overview'],
#                 'poster_path': movie['poster_path'],
#                 'genres': json.dumps(genres, ensure_ascii=False)
#             }
#             movie_data.append(data)

#     return movie_data



# # 1부터 500 페이지까지의 영화 데이터를 가져와 데이터베이스에 저장
# for page in range(101,501):
#     movie_data = get_movie_data(page)

#     for data in movie_data:
#         cur.execute('''
#             INSERT INTO movies (
#                 movie_id, title, release_date, popularity,
#                 vote_average, vote_count, overview, poster_path, 
#                 genres
#             ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
#             ON CONFLICT (movie_id)
#             DO UPDATE SET (title, release_date, popularity,
#                 vote_average, vote_count, overview, poster_path, 
#                 genres) = (excluded.title, excluded.release_date, excluded.popularity,
#                 excluded.vote_average, excluded.vote_count, excluded.overview, excluded.poster_path, 
#                 excluded.genres)
#         ''', (
#             data['movie_id'], data['title'], data['release_date'],
#             data['popularity'], data['vote_average'], 
#             data['vote_count'], data['overview'],
#             data['poster_path'], data['genres']
#         ))


# # 변경 사항 저장 및 연결 종료
#     conn.commit()
# conn.close()



# # 데이터베이스 연결
# conn = sqlite3.connect('movies.db') #db가 없는 경우 새로 생성
# cur = conn.cursor()

# # movie_details 테이블 생성
# cur.execute("""
#     CREATE TABLE IF NOT EXISTS movie_details (
#     movie_id INTEGER PRIMARY KEY,
#     cast TEXT,
#     crew TEXT,
#     keywords TEXT
#     )""")

# # api로 데이터 가져오기
# def get_movie_data(page):
#     request_url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page={page}"
#     response = requests.get(request_url)
#     movies = response.json()

#     movie_data = []
#     for movie in movies['results']:
#         if movie.get('release_date', ''):
#             movie_id = movie['id']
#             movie_data.append(movie_id)

#     return movie_data

# # 영화 데이터 가져오기
# movie_data = []
# for page in range(2, 501):
#     movie_data += get_movie_data(page)

# # 영화 세부 정보 가져와서 데이터베이스에 저장
# for movie_id in movie_data:
#     # 키워드 정보 조회
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}/keywords?api_key={TMDB_API_KEY}&language=en-US"
#     response = requests.get(url)
#     keywords = response.json()
#     keywords_json = json.dumps(keywords, ensure_ascii=False)

#     # 출연진 및 제작진 정보 조회
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={TMDB_API_KEY}&language=en-US"
#     response = requests.get(url)
#     credits = response.json()
#     cast_json = json.dumps(credits['cast'], ensure_ascii=False)
#     crew_json = json.dumps(credits['crew'], ensure_ascii=False)

#     # movie_details 테이블에 데이터 삽입
#     cur.execute('''
#         INSERT INTO movie_details (
#             movie_id, cast, crew, keywords
#         ) VALUES (?, ?, ?, ?)
#             ON CONFLICT (movie_id)
#             DO UPDATE SET (cast, crew, keywords) = 
#             (excluded.cast, excluded.crew, excluded.keywords)
#     ''', (
#         movie_id, cast_json, crew_json, keywords_json
#     ))
#     conn.commit()

# # 연결 종료
# conn.close()