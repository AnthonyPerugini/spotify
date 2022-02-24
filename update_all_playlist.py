import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import defaultdict

os.environ["SPOTIPY_REDIRECT_URI"] = 'http://localhost:8080/callback'


scope = "user-library-read, playlist-modify-public"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


playlists_to_pull = ['two perceptrons', 'especially you', 'pineapple pizzas', 'some pandora you are', 'koala tea', 'lookin sharp // feelin flat', 'kisses', 'run A way', 'tension', 'dreads', 'berries', 'filth', 'climb_rap']

def main():
    # build playlist_name -> playlist_id hashmap
    playlist_names_and_ids = defaultdict()
    for playlist in sp.current_user_playlists()['items']:
        if playlist['name'] in playlists_to_pull:
            playlist_names_and_ids[playlist['name']] = playlist['id']


    # build set of all unique songs and their ids
    unique_songs = defaultdict()
    song_name_to_id = defaultdict()
    for playlist_name, uuid in playlist_names_and_ids.items():
        playlist = sp.playlist_items(uuid)
        for song in playlist['items']:
            song_name = song['track']['name']
            song_id = song['track']['id']
            if not song_name in unique_songs:
                unique_songs[song_name] = playlist_name
            else:
                print(f'{song_name} :: DUPLICATE {unique_songs[song_name]} -> {playlist_name}')
                
            if not song_name in song_name_to_id:
                song_name_to_id[song_name] = song_id

    # clear old 'All' playlist and add new songs in batches of 100 (max chunk)
    sp.playlist_replace_items('0hX5pNTy9VgKqQk8Zyr3F2', [])
    for chunk in divide_chunks(list(song_name_to_id.values()), 100):
        sp.playlist_add_items('0hX5pNTy9VgKqQk8Zyr3F2', chunk)


def divide_chunks(l, n):
      
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]


if __name__ == '__main__':
    main()
