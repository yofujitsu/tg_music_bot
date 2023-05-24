from yandex_music import Client
client = Client().init()

class Track():
    def __init__(self ,id,tr, title,author):
        self.id = id
        self.tr=tr
        self.title=title
        self.author=author
    def getTr(self):
        return self.tr
    def getTitle(self):
        return self.title
    def getAuthor(self):
        return self.author

class MyPerson():
    mytrack = []
    count=5
    page=1
    curr_playlist = ''
    curr_album = 0
    curr_artist = ''
    TOKEN = ''
    def __init__(self):
        self.client = Client().init()

    def setTOKEN(self, TOKEN):
        self.TOKEN = TOKEN
        self.client = Client(TOKEN).init()

    def setPlaylist(self, playId):
        self.curr_playlist = playId

    def setArtist(self, aId):
        self.curr_artist = aId

    def setAlbum(self, albumId):
        self.curr_album = albumId

    def getTOKEN(self):
        return self.TOKEN

    type_to_name = {
        'track': 'трек',
        'artist': 'исполнитель',
        'album': 'альбом',
        'playlist': 'плейлист',
        'video': 'видео',
        'user': 'пользователь',
        'podcast': 'подкаст',
        'podcast_episode': 'эпизод подкаста'
    }

    def get_likes_tracks(self, page=0):
        if page==0:
            self.page=1
        else:
            self.page+=page
        self.mytrack = []
        tracks = self.client.users_likes_tracks()
        for i in range(0+self.count*self.page-5,self.count*self.page):
            print(0+self.count*self.page-5,self.count*self.page, self.page)
            self.mytrack.append(Track(int(tracks[i].id),tracks[i],self.client.tracks(tracks[i].id)[0].title,", ".join(self.client.tracks(tracks[i].id)[0].artists_name())))
        return self.mytrack

    def download(self,id):
        id = int(id)
        title = ''
        for i in self.mytrack:
            print(i.id, id, type(i.id), type(id))
            if (i.id==id):
                print("win")
                print(type(i))
                print(id)
                try:
                    i.tr.fetch_track().download(i.author+" - "+i.title+".mp3")
                except AttributeError: i.tr.download(i.author+" - "+i.title+".mp3")
                title = i.author+" - "+i.title+".mp3"
                break
        return title

    def search(self, query):
        search_result = client.search(query)
        text = [f'Результаты по запросу "{query}":', '']
        best_result_text = ''
        if search_result.best:
            type_ = search_result.best.type
            best = search_result.best.result
            print(best)

            text.append(f'❗️Лучший результат: {self.type_to_name.get(type_)}')

            if type_ in ['track', 'podcast_episode']:
                artists = ''
                if best.artists:
                    artists = ' - ' + ', '.join(artist.name for artist in best.artists)
                best_result_text = best.title + artists
            elif type_ == 'artist':
                best_result_text = best.name
            elif type_ in ['album', 'podcast']:
                best_result_text = best.title
            elif type_ == 'playlist':
                best_result_text = best.title
            elif type_ == 'video':
                best_result_text = f'{best.title} {best.text}'

            text.append(f'Содержимое лучшего результата: {best_result_text}\n')

        if search_result.artists:
            text.append(f'Исполнителей: {search_result.artists.total}')
        if search_result.albums:
            text.append(f'Альбомов: {search_result.albums.total}')
        if search_result.tracks:
            text.append(f'Треков: {search_result.tracks.total}')
        if search_result.playlists:
            text.append(f'Плейлистов: {search_result.playlists.total}')
        if search_result.videos:
            text.append(f'Видео: {search_result.videos.total}')
        text.append('')
        print('\n'.join(text))

        return [self.type_to_name.get(type_), best]

    def search_res(self, query):
        search_result = client.search(query)
        text = [f'Результаты по запросу "{query}":', '']
        best_result_text = ''
        if search_result.best:
            type_ = search_result.best.type
            best = search_result.best.result
            print(best)

            text.append(f'❗️Лучший результат: {self.type_to_name.get(type_)}')

            if type_ in ['track', 'podcast_episode']:
                artists = ''
                if best.artists:
                    artists = ' - ' + ', '.join(artist.name for artist in best.artists)
                best_result_text = best.title + artists
            elif type_ == 'artist':
                best_result_text = best.name
            elif type_ in ['album', 'podcast']:
                best_result_text = best.title
            elif type_ == 'playlist':
                best_result_text = best.title
            elif type_ == 'video':
                best_result_text = f'{best.title} {best.text}'

            text.append(f'Содержимое лучшего результата: {best_result_text}\n')

        if search_result.artists:
            text.append(f'Исполнителей: {search_result.artists.total}')
        if search_result.albums:
            text.append(f'Альбомов: {search_result.albums.total}')
        if search_result.tracks:
            text.append(f'Треков: {search_result.tracks.total}')
        if search_result.playlists:
            text.append(f'Плейлистов: {search_result.playlists.total}')
        if search_result.videos:
            text.append(f'Видео: {search_result.videos.total}')
        text.append('')
        return '\n'.join(text)

    # def provide_search_info(self, query):



    def get_playlists(self):
        res=[]
        for i in self.client.usersPlaylistsList():
            res.append([i.title,i.playlistId.split(":")[1]])
        return res

    def get_tracks_by_playlist(self,page=0):
        if page==0:
            self.page=1
        else:
            self.page+=page
        tracks=self.client.usersPlaylists(self.curr_playlist).tracks
        for i in tracks: print(type(i))
        self.mytrack = []
        for i in range(0 + self.count * self.page - 5, self.count * self.page):
            if i<len(tracks):
                print(0 + self.count * self.page - 5, self.count * self.page, self.page)
                self.mytrack.append(Track(int(tracks[i].id), tracks[i], self.client.tracks(tracks[i].id)[0].title,
                                          ", ".join(self.client.tracks(tracks[i].id)[0].artists_name())))
        return self.mytrack

    def get_albums(self):
        res = []
        albums = self.client.users_likes_albums()
        for i in albums:
            res.append([str(i.album.artists_name())[2:-2], i.album.title, i.album.id])
        return res

    def get_tracks_by_album(self, page=0):
        if page==0:
            self.page=1
        else:
            self.page+=page
        album=self.client.albums_with_tracks(self.curr_album)
        album_tracks = []
        print(album.volumes)
        for i, volume in enumerate(album.volumes):
            if len(album.volumes) > 1:
                album_tracks.append(f'💿 Диск {i + 1}')
            album_tracks += volume
        self.mytrack = []
        for track in album_tracks:
            artists = ''
            if track.artists:
                artists = ' - ' + ', '.join(artist.name for artist in track.artists)
                print(track.title + artists)
        print(len(album_tracks))
        for i in album_tracks: print(type(i))
        for i in range(0 + self.count * self.page - 5, self.count * self.page):
            if i<len(album_tracks):
                # print(0 + self.count * self.page - 5, self.count * self.page, self.page)
                self.mytrack.append(Track(int(album_tracks[i].id), album_tracks[i], self.client.tracks(album_tracks[i].id)[0].title,
                                          ", ".join(self.client.tracks(album_tracks[i].id)[0].artists_name())))
        return self.mytrack

    def add_to_favs(self, id):
        return self.client.users_likes_tracks_add(id)

    def download_by_link(self, id):
        self.mytrack = []
        id = int(id)
        title = ''
        track = self.client.tracks(id)
        self.mytrack.append(
            Track(int(track[0].id), track[0], track[0].title,
                  ", ".join(track[0].artists_name())))
        for i in self.mytrack:
            print(i.id, id, type(i.id), type(id))
            if (i.id == id):
                print("win")
                print(type(i))
                print(id)
                try:
                    i.tr.fetch_track().download(i.author + " - " + i.title + ".mp3")
                except AttributeError:
                    i.tr.download(i.author + " - " + i.title + ".mp3")
                title = i.author + " - " + i.title + ".mp3"
                break
        return title

    def get_tracks_by_artist(self, page=0):
        if page==0:
            self.page=1
        else:
            self.page+=page
        tracks=self.client.artistsTracks(self.curr_artist)
        for i in tracks: print(type(i))
        self.mytrack = []
        for i in range(0 + self.count * self.page - 5, self.count * self.page):
            if i<len(tracks):
                print(0 + self.count * self.page - 5, self.count * self.page, self.page)
                self.mytrack.append(Track(int(tracks[i].id), tracks[i], self.client.tracks(tracks[i].id)[0].title,
                                          ", ".join(self.client.tracks(tracks[i].id)[0].artists_name())))
        return self.mytrack

