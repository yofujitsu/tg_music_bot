from yandex_music import Client
TOKEN='AQAAAAASg-EiAAG8Xth12jSrvkhtqzxHtyTafzo'
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
    # def __init__(self,TOKEN):
    #     self.TOKEN=TOKEN
    #     self.client = Client(TOKEN).init()

    def setTOKEN(self, TOKEN):
        self.TOKEN = TOKEN
        self.client = Client(TOKEN).init()

    def setPlaylist(self, playId):
        self.curr_playlist = playId

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
        for i in self.mytrack:
            if (i.id==id):
                print("win")
                i.tr.fetch_track().download(i.author+" - "+i.title+".mp3")
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

    def test(self):
        print(self.client.usersPlaylistsList()[0].playlistId)
        print(self.client.usersPlaylists(1006).tracks[1].track.title)

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
        self.mytrack = []
        for i in range(0 + self.count * self.page - 5, self.count * self.page):
            if i<len(tracks):
                print(0 + self.count * self.page - 5, self.count * self.page, self.page)
                self.mytrack.append(Track(int(tracks[i].id), tracks[i], self.client.tracks(tracks[i].id)[0].title,
                                          ", ".join(self.client.tracks(tracks[i].id)[0].artists_name())))
        return self.mytrack



# '''Сюда нужно передать токен'''
# person=MyPerson()
# person.get_lickes_tracks()
# for i in range(len(person.mytrack)):
#     print(person.mytrack[i].id,person.mytrack[i].title,person.mytrack[i].author)
# person.download(person.mytrack[0].id)






# Track={
#     "tr",
#     "title",
#     "author"
# }
#
# track=client.users_likes_tracks()[0]
# print(client.tracks(track.id)[0].title)
# person=MyPerson('AQAAAAASg-EiAAG8Xth12jSrvkhtqzxHtyTafzo')
# print(person.get_lickes_tracks()[0].author)
# MyPerson.page=3
# MyPerson.count=5
# person.test()
# list=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
# for i in range(0+MyPerson.count*MyPerson.page-5,MyPerson.count*MyPerson.page):
#     print(list[i])

# MyPerson.page=3
# MyPerson.count=5
# list=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
# for i in range(0+MyPerson.count*MyPerson.page-5,MyPerson.count*MyPerson.page):
#     print(list[i])