import streamlit as st
import pickle
import pandas as pd
import requests
import os


def fetch_poster(movie_id):
    api_key = st.secrets.get("TMDB_API_KEY") or os.getenv("TMDB_API_KEY")
    if not api_key:
        # No API key configured; skip poster fetching
        return ""
    try:
        response = requests.get(
            'https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'.format(movie_id, api_key),
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if not poster_path:
            return ""
        return "https://image.tmdb.org/t/p/w500" + poster_path
    except Exception:
        return ""



def recommend(movie, movies, similarity):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


@st.cache_data(show_spinner=False)
def load_data():
    try:
        with open('movie_dict.pkl', 'rb') as f:
            movies_dict = pickle.load(f)
        with open('similarity.pkl', 'rb') as f:
            similarity = pickle.load(f)
    except Exception as e:
        st.error("Failed to load data files. Ensure valid 'movie_dict.pkl' and 'similarity.pkl' are present in the app directory. Error: {}".format(e))
        st.stop()

    movies_df = pd.DataFrame(movies_dict)
    required_columns = {'title', 'movie_id'}
    if not required_columns.issubset(set(movies_df.columns)):
        st.error("Data is missing required columns: {}".format(', '.join(sorted(required_columns))))
        st.stop()

    return movies_df, similarity


movies, similarity = load_data()

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Select a movie",
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name, movies, similarity)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        if posters[0]:
            st.image(posters[0])

    with col2:
        st.text(names[1])
        if posters[1]:
            st.image(posters[1])

    with col3:
        st.text(names[2])
        if posters[2]:
            st.image(posters[2])

    with col4:
        st.text(names[3])
        if posters[3]:
            st.image(posters[3])

    with col5:
        st.text(names[4])
        if posters[4]:
            st.image(posters[4])


