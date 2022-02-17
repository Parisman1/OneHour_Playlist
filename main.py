import spotipy
from spotipy.oauth2 import SpotifyOAuth

#from a playlist return
#['tracks']['items']['track']['name']
#['tracks']['items']['track']['duration_ms']
#['tracks']['items']['track']['id']

def initiate():
    scope = "user-library-read playlist-modify-public playlist-read-private"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    name = sp.user('1215681200')['id']

    one_id = '1tioZqeUfRNMvmTbYJVx2a'
    back_id = '451VYAgklW4Yzqljkdp47O'

    return name, sp, one_id, back_id

def list_my_playlists(name):
    playlists = sp.user_playlists(name)

    while playlists:
        for playlist in playlists['items']:
            print("%s %s " % (playlist['id'], playlist['name']))
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None

def print_songs_in_playlist(sp, name, one_id, back_id):
    results = sp.user_playlist(user=name, playlist_id=one_id, fields='tracks')
    playlist = results['tracks']
    playlist_items = playlist['items']
    for track_item in playlist_items:
        song = track_item['track']['name']
        print(song)

def clear_playlist(sp, name, one_id, back_id):
    song_list = []

    results = sp.user_playlist(user=name, playlist_id=one_id, fields='tracks')
    playlist = results['tracks']
    playlist_items = playlist['items']
    for track_item in playlist_items:
        song_list.append(track_item['track']['id'])

    sp.playlist_remove_all_occurrences_of_items(one_id, song_list)

def init_valList(size):
    valList = [60 for i in range(size)]
    return valList


def refill_playlist(sp, name, one_id, back_id, valList):
    msList  = []
    idList  = []
    posList = []
    endList = []

    results = sp.user_playlist(user=name, playlist_id=back_id, fields='tracks')
    playlist_items = results['tracks']['items']
    for track_item in playlist_items:
        msList.append(track_item['track']['duration_ms'])
        idList.append(track_item['track']['id'])

    # this should only run if the program has never run
    if len(valList) == 0:
        valList = init_valList(len(idList))

    posList = printknapSack(3600000, msList, valList, len(valList))

    for pos in posList:
        endList.append(idList[pos])

    sp.playlist_add_items(one_id, endList)


# W is duration wanted aka 60 min
# wt is list of weights
# val is abstract val that will be reduced if the song has been used and will be increased if not used
# n is len(val)
def printknapSack(W, wt, val, n):
    toUseList = []

    K = [[0 for w in range(W + 1)]
            for i in range(n + 1)]
             
    # Build table K[][] in bottom
    # up manner
    for i in range(n + 1):
        for w in range(W + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif wt[i - 1] <= w:
                K[i][w] = max(val[i - 1] + K[i - 1][w - wt[i - 1]], K[i - 1][w])
            else:
                K[i][w] = K[i - 1][w]
 
    # stores the result of Knapsack
    res = K[n][W]
    #print(res)
     
    w = W
    for i in range(n, 0, -1):
        if res <= 0:
            break
        # either the result comes from the
        # top (K[i-1][w]) or from (val[i-1]
        # + K[i-1] [w-wt[i-1]]) as in Knapsack
        # table. If it comes from the latter
        # one/ it means the item is included.
        if res == K[i - 1][w]:
            continue
        else:
 
            # This item is included.
            #print(wt[i - 1])
            toUseList.append(i-1)
             
            # Since this weight is included
            # its value is deducted
            res = res - val[i - 1]
            w = w - wt[i - 1]

    return toUseList

if __name__ == "__main__":

    name, sp, one_id, back_id = initiate()
    valList = []

    clear_playlist(sp, name, one_id, back_id)
    refill_playlist(sp, name, one_id, back_id, valList)
    #list_my_playlists(name)
    