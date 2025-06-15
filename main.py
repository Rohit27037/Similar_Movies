import pickle

import pandas as pd
import requests
import streamlit as st


def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=20a6f33f12f7aad5e1bb817d4fa48138')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie, num_movies=10):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:num_movies + 1]

    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.markdown(
    """
    <style>
    .main {
        max-width: 1600px;
        margin: 0 auto;
        padding: 10px;
        text-align: center;
    }
    .stTitle {
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 40px; 
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 8px 16px;
        border-radius: 12px;
        border: none;
        cursor: pointer;
        font-size: 1rem;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stText {
        color: #00ff00;
        font-weight: bold;
        text-align: center;
    }
    .poster {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .poster img {
        width: 100%;
        max-width: 200px;
        border-radius: 8px;
    }
    .poster-text {
        text-align: center;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎬 Similar Movies")
st.markdown("Find similar movies based on your favorite one!")

selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movies['title'].values
)

num_movies = st.slider('Number of Movies to Recommend', 5, 10, 10)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name, num_movies)
    cols = st.columns(5)

    for i, col in enumerate(cols):
        if i < len(names):
            with col:
                st.markdown(
                    f"""
                    <div class="poster">
                        <img src="{posters[i]}" alt="{names[i]}">
                        <div class="poster-text">{names[i]}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    if len(names) > 5:
        cols = st.columns(5)
        for i, col in enumerate(cols):
            if i + 5 < len(names):
                with col:
                    st.markdown(
                        f"""
                        <div class="poster">
                            <img src="{posters[i + 5]}" alt="{names[i + 5]}">
                            <div class="poster-text">{names[i + 5]}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )





