from yandex_music import Client
# client=Client(TOKEN).init()
# track=client.users_likes_tracks()[0]
# track.fetch_track().download("askldjhl.mp3")
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
    def __init__(self,TOKEN):
        self.TOKEN=TOKEN
        self.client = Client(TOKEN).init()


    def get_lickes_tracks(self):
        if (len(self.mytrack)==0):
            tracks = self.client.users_likes_tracks()
            for i in range(0+MyPerson.count*MyPerson.page-5,MyPerson.count*MyPerson.page):
                self.mytrack.append(Track(tracks[i].id,tracks[i],self.client.tracks(tracks[i].id)[0].title,"".join(self.client.tracks(tracks[i].id)[0].artists_name())))
        return self.mytrack
    def download(self,id):
        for i in self.mytrack:
            if (i.id==id):
                print("win")
                i.tr.fetch_track().download(i.author+" - "+i.title+".mp3")


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
# person=MyPerson("y0_AgAAAAA-m1eKAAG8XgAAAADjdu60-k8-pH7FQ2u9v4GHmaRAFx_JP60")
# print(person.get_lickes_tracks()[0].author)
# MyPerson.page=3
# MyPerson.count=5
# list=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
# for i in range(0+MyPerson.count*MyPerson.page-5,MyPerson.count*MyPerson.page):
#     print(list[i])