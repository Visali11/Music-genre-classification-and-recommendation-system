import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = "12ad5e4edb954784a59acf30f4decca2"
CLIENT_SECRET = "fae7554fce664af99c75152b1d7a2775"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        print(album_cover_url)
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"


st.header('Music genre classification & Recommendation System')
df = pickle.load(open('mu (1).pkl','rb'))
similarity = pickle.load(open('similer (1).pkl','rb'))

def recommendation(df, song_title, n=11):
    song_genre = df.loc[df['Title'] == song_title, 'Top Genre'].values[0]
    genre_songs = df[df['Top Genre'] == song_genre]
    if len(genre_songs) < n:
            n = len(genre_songs)  # Limit n to the available songs
            st.write(f"There are only {n} songs in the '{song_genre}' genre.")

    recommended_songs = genre_songs.sample(n)['Title'].tolist()
    return song_genre, recommended_songs

    

music_list = df['Title'].values
selected_song = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)


if st.button('Get Recommendations'):
    # Get the text of the selected song
    selected_song = df.loc[df['Title'] == selected_song, 'Title'].iloc[0]
    
    # Call the recommendation function with df as argument
    song_genre, recommended_songs = recommendation(df, selected_song)
    
    # Display recommended songs
    st.write("Genre based on the input song:", song_genre)
    st.write("Recommended songs")
    st.write(recommended_songs)
