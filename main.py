import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os.path

# from a playlist return
# ['tracks']['items']['track']['name']
# ['tracks']['items']['track']['duration_ms']
# ['tracks']['items']['track']['id']


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
    print("clearing playlist")
    song_list = []

    results = sp.user_playlist(user=name, playlist_id=one_id, fields='tracks')
    playlist = results['tracks']
    playlist_items = playlist['items']
    for track_item in playlist_items:
        song_list.append(track_item['track']['id'])

    sp.playlist_remove_all_occurrences_of_items(one_id, song_list)
    print("playlist is cleared")


def init_valList(size):
    valList = [50 for i in range(size)]
    # print(type(valList[1]))
    return valList


def refill_playlist(sp, name, one_id, back_id, valList, new):
    print("refilling playlist")
    msList = []
    idList = []
    posList = []
    endList = []
    bruh = True

    results = sp.user_playlist(user=name, playlist_id=back_id, fields='tracks')
    playlist_items = results['tracks']['items']
    for track_item in playlist_items:
        msList.append(track_item['track']['duration_ms'])
        idList.append(track_item['track']['id'])

    # this should only run if the program has never run
    if new:
        valList = init_valList(len(idList))

    # print("len of valList = ", len(valList))
    # print("type of val with file = ", type(valList[1]))
    print("Starting knapsack")
    posList = printknapSack(3600000, msList, valList, len(valList))
    print("Ending knapsack")

    print("Fixing song values")
    # print(len(valList))
    for i in range(len(valList)):
        for pos in posList:
            if i == pos:
                # print('reducing ', i, '(', pos, ') by 5')
                valList[i] = valList[i] - 10
                bruh = False
                break
        if bruh:
            valList[i] = valList[i] + 10
            # print('increasing ', i, ' by 5')
        else:
            bruh = True
    print("song values adjusted")

    for pos in posList:
        endList.append(idList[pos])

    print("adding items to playlist")
    sp.playlist_add_items(one_id, endList)

    print("playlist refilled")
    return valList


# W is duration wanted aka 60 min
# wt is list of weights
# val is abstract val that will be reduced if the song has been used and will
# be increased if not used
# n is len(val)
def printknapSack(W, wt, val, n):
    toUseList = []

    K = [[0 for w in range(W + 1)] for i in range(n + 1)]

    # Build table K[][] in bottom
    # up manner
    for i in range(n + 1):
        for w in range(W + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif wt[i - 1] <= w:
                K[i][w] = max(val[i - 1]+K[i - 1][w - wt[i - 1]], K[i - 1][w])
            else:
                K[i][w] = K[i - 1][w]

    # stores the result of Knapsack
    res = K[n][W]
    # print(res)

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
            # print(wt[i - 1])
            toUseList.append(i-1)

            # Since this weight is included
            # its value is deducted
            res = res - val[i - 1]
            w = w - wt[i - 1]

    return toUseList


if __name__ == "__main__":

    name, sp, one_id, back_id = initiate()
    fileList = []
    valList = []
    songs_used = []
    new = False

    if os.path.exists('Songs.txt'):
        with open('Songs.txt', 'r') as f:
            fileList = f.readlines()
        for val in fileList:
            valList.append(int(val))
    else:
        f = open("Songs.txt", 'w')
        f.close()
        new = True

    clear_playlist(sp, name, one_id, back_id)
    valList = refill_playlist(sp, name, one_id, back_id, valList, new)

    with open('Songs.txt', 'w') as f:
        for val in valList:
            f.write(str(val))
            f.write('\n')

    # list_my_playlists(name)
