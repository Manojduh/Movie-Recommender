import streamlit as st
import pickle
import pandas as pd
import requests

# ✅ Set page config FIRST
st.set_page_config(page_title="Movie Recommender", page_icon="🎥", layout="wide")

# Load data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# TMDB API key
TMDB_API_KEY = 'YOUR_TMDB_API_KEY'  # Replace with your TMDB API key

# Function to fetch poster using TMDB API
def fetch_poster(movie_title):
    TMDB_API_KEY = "7723e6613eb30932b5aa1ca686319676"  # ✅ Correct

    url = f'https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}'
    response = requests.get(url)
    data = response.json()
    if data['results']:
        poster_path = data['results'][0].get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return "https://via.placeholder.com/500x750.png?text=No+Image"

# Recommend function
def recommend(movie):
    movie = movie.lower()
    try:
        movie_index = movies[movies['title_x'].str.lower() == movie].index[0]
    except IndexError:
        return [], []
    
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movie_list:
        title = movies.iloc[i[0]]['title_x']
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster(title))
    return recommended_movies, recommended_posters

# Sidebar
st.sidebar.title("🎬 Movie Recommender")
st.sidebar.markdown("Find similar movies based on your choice.")

# Title
st.markdown('<h1 style="text-align:center; color:#FF6347;">🎥 Movie Recommendation System</h1>', unsafe_allow_html=True)

# Movie list
movie_titles = movies['title_x'].tolist()
movie_name = st.selectbox('Select a movie you like:', movie_titles)

# Show recommendations
if st.button('Show Recommendations'):
    if movie_name:
        recommendations, posters = recommend(movie_name)
        if recommendations:
            st.markdown('<h2 style="text-align:center;">Recommended Movies</h2>', unsafe_allow_html=True)
            cols = st.columns(5)
            for idx, col in enumerate(cols):
                col.image(posters[idx])
                col.markdown(f"<p style='text-align:center;font-weight:bold;'>{recommendations[idx]}</p>", unsafe_allow_html=True)
        else:
            st.warning("Movie not found. Please try another.")
    else:
        st.warning("Please select a movie.")

# Footer
st.markdown("""
    <div style="text-align:center; margin-top:40px; color:#888;">
        Made with ❤️ by Movie Recommender Team
    </div>
""", unsafe_allow_html=True)
