import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1MWQzOTMyNjRjYzZiZmUxYTg4YjlkOWFkOTYyMDY3OCIsIm5iZiI6MTcyMTk4NDU5Ni43MDk3OTgsInN1YiI6IjY2OThmNjU3NjQ1OWRlNmU5ODNhYjYzMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.fFiMiICC9P0MNcWie64WM59bWtCnad9A27tHR3BJcfg"
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movies.iloc[i[0]].movie_id))
    return recommended_movies, recommended_movies_poster


st.title("Movie Recommender System")

selected_movie_name = st.selectbox('Enter the movie name ', movies['title'].values)
if st.button("Recommend"):
    names, poster = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(poster[0])

    with col2:
        st.text(names[1])
        st.image(poster[1])

    with col3:
        st.text(names[2])
        st.image(poster[2])

    with col4:
        st.text(names[3])
        st.image(poster[3])

    with col5:
        st.text(names[4])
        st.image(poster[4])
