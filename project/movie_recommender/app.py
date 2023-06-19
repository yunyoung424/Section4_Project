from flask import Flask, render_template, request
import sqlite3
import pickle
import pandas as pd
import threading

app = Flask(__name__)

# 스레드 로컬 데이터베이스 연결
local_conn = threading.local()

def get_db():
    # 현재 스레드에 연결된 데이터베이스 가져오기
    if not hasattr(local_conn, 'conn'):
        local_conn.conn = sqlite3.connect('movies.db')
    return local_conn.conn

@app.teardown_appcontext
def close_db(error):
    # 데이터베이스 연결 종료
    if hasattr(local_conn, 'conn'):
        local_conn.conn.close()

# 모델 로드
movies = pickle.load(open('movies.pkl', 'rb'))
cosine_sim = pickle.load(open('cosine_sim2.pkl', 'rb'))

def get_recommendations(title):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    images = []
    titles = []

    for i in movie_indices:
        poster_path = movies['poster_path'].iloc[i]
        image_url = f"https://image.tmdb.org/t/p/w342{poster_path}"
        images.append(image_url)

        movie_title = movies['title'].iloc[i]
        titles.append(movie_title)

    return images, titles


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/recommendations', methods=['POST'])
def recommendations():
    title = request.form['title']
    recommended_movies = get_recommendations(title)

    # 스레드 로컬 데이터베이스 연결 사용
    conn = get_db()
    cur = conn.cursor()

    # SQL 쿼리 생성 및 실행
    placeholders = ', '.join(['?'] * len(recommended_movies[0]))
    query = f"SELECT title, release_date, poster_path FROM movies WHERE title IN ({placeholders})"
    cur.execute(query, recommended_movies[1])

    recommended_movies_data = cur.fetchall()

    # 이미지 URL을 포함한 영화 정보를 템플릿에 전달
    recommended_movies_with_images = []
    for movie, image_url in zip(recommended_movies_data, recommended_movies[0]):
        recommended_movies_with_images.append((*movie, image_url))

    input_movie = movies.loc[movies['title'] == title, ['title', 'release_date', 'poster_path']].values[0]

    return render_template('recommendations.html', title=title, input_movie=input_movie, recommended_movies=recommended_movies_with_images)



if __name__ == '__main__':
    app.run()
