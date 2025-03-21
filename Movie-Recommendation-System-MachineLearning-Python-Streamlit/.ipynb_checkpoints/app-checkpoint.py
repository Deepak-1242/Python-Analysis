import streamlit as st
import pandas as pd 
import joblib
import requests

movies_dict = joblib.load('./movies_dict.pkl')

movies = pd.DataFrame(movies_dict)

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=d1aa405518bcd86047c245cdc2bfe4e5'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    

def recommend(movie):
    movies_index = movies[movies.title == movie].index[0]
    distance = similarity[movies_index]
    recommended_movies = sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:11]

    recommended_movies_list = []
    movies_posters=[]
    for i in recommended_movies:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_list.append(movies.iloc[i[0]].title)
        movies_posters.append(fetch_poster(movie_id))
    return recommended_movies_list,movies_posters

similarity = joblib.load('./similarity.pkl')

st.header("Movie Recommendation System")

selected_option = st.selectbox("Enter the movie name: ", movies.title.values)

if st.button("Recommend"):
    names,posters = recommend(selected_option)

    col1,col2,col3,col4,col5,col6,col7,col8,col9,col10 = st.columns(10)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
    with col6:
        st.text(names[5])
        st.image(posters[5])
    with col7:
        st.text(names[6])
        st.image(posters[6])
    with col8:
        st.text(names[7])
        st.image(posters[7])
    with col9:
        st.text(names[8])
        st.image(posters[8])
    with col10:
        st.text(names[9])
        st.image(posters[9])
    