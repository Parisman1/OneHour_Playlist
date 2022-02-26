# OneHour_Playlist

This project uses spotipy to connect to the Spotify Api

first you have to define 2 playlists, one to act as the wanted playlist and one playlist to use as a "backlog" 

the program pulls from the backlog using 0/1 knapsack to fill the 1st playlist with songs up to the desired length 

when a song is used the "value" of that song is reduced and when a song isnt used its 'value' is increased to create a cycle of songs each time you run the program
