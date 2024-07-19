# Download the dataset

import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import re
import random

# Load the dataset
ratings = pd.read_csv('ratings.dat', sep='::', header=None, engine='python',
                      names=['user_id', 'movie_id', 'rating', 'timestamp'])
movies = pd.read_csv('movies.dat', sep='::', header=None, engine='python',
                     names=['movie_id', 'title', 'genres'], encoding='latin-1')


# Create a user-item matrix
user_item_matrix = ratings.pivot(index='user_id', columns='movie_id', values='rating').fillna(0)

# Calculate cosine similarity between items
item_similarity = cosine_similarity(user_item_matrix.T)
item_similarity_df = pd.DataFrame(item_similarity, index=user_item_matrix.columns, columns=user_item_matrix.columns)

def get_movie_id(movie_title):
    try:
        movie_id = movies[movies['title'].str.contains(movie_title, case=False, na=False)]['movie_id'].values[0]
        return movie_id
    except IndexError:
        return None

def get_random_movies(num_movies=5):
    random_movie_ids = random.sample(list(movies['movie_id']), num_movies)
    random_movie_titles = movies[movies['movie_id'].isin(random_movie_ids)]['title'].values
    return random_movie_titles

def get_recommendations(movie_title, num_recommendations=5):
    movie_id = get_movie_id(movie_title)
    if movie_id is None:
        random_movies = get_random_movies(num_recommendations)
        return f"Movie '{movie_title}' not found in the database. Here are some random recommendations instead:\n" + ',\n '.join(random_movies)

    similar_movies = item_similarity_df[movie_id].sort_values(ascending=False).index[1:num_recommendations+1]
    recommended_titles = movies[movies['movie_id'].isin(similar_movies)]['title'].values
    return recommended_titles

def chatbot_response(user_input):
    user_input = user_input.lower()

    # Define patterns and corresponding responses
    patterns = {
        r'hello|hi': "Hello! How can I help you today?",
        r'how are you': "I'm just a bot, but I'm doing great! How about you?",
        r'what is your name|who are you': "I'm a simple chatbot created to assist you.",
        r'help|can you recommend a movie|movie': "Sure, I'm here to help! You can ask me for movie recommendations by telling me a movie you like. For example, 'I like Titanic'.",
        r'bye|goodbye': "Goodbye! Have a great day!"
    }

    for pattern, response in patterns.items():
        if re.search(pattern, user_input):
            return response
    
    # Check if the user is asking for recommendations
    if re.search(r'i like .+', user_input):
        movie_title = re.search(r'i like (.+)', user_input).group(1)
        recommendations = get_recommendations(movie_title)
        if isinstance(recommendations, str):
            return recommendations
        if recommendations.size > 0:
            rec_movies = ',\n '.join(recommendations)
            return f"If you like '{movie_title}', you might also enjoy:\n {rec_movies}."
        else:
            return "I couldn't find any recommendations for this movie."
    
    # Default response if no pattern matches
    return "I'm sorry, I didn't understand that. Can you please rephrase?"

# Streamlit app
st.title('Chatbot with Movie Recommendation System')

st.write('Hello! I am a simple chatbot. You can ask me for movie recommendations by telling me a movie you like. For example, "I like Titanic".')

# Initialize session state for user input
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

def submit():
    st.session_state.response = chatbot_response(st.session_state.user_input)
    st.session_state.user_input = ""

user_input = st.text_input("You: ", key="user_input", on_change=submit)

if 'response' in st.session_state:
    st.text_area("Chatbot:", value=st.session_state.response, height=200)

if user_input.lower() in ['bye', 'goodbye']:
    st.write("Chatbot: Goodbye! Have a great day!")
