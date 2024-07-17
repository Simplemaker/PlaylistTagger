from main import process_section

class Song:
    def __init__(self, title=None, artist=None, album=None, art=None, track=None, yt=None):
        self.title = title
        self.artist = artist
        self.album = album
        self.art = art
        self.track = track
        self.yt = yt

    def __str__(self):
        return (f"Song(title={self.title}, artist={self.artist}, album={self.album}, "
                f"art={self.art}, track={self.track}, yt={self.yt})")
    
    def download(self):
        process_section({
            "title": self.title,
            "artist": self.artist,
            "yt":self.yt,
            "album": self.album,
            "art":self.art,
            "track":str(self.track)
        })

class SongBuilder:
    def __init__(self, returnFunction=None, returnValue=None):
        self.rf = returnFunction
        self.rv = returnValue
        self.song = Song()

    def title(self, title):
        self.song.title = title
        return self

    def artist(self, artist):
        self.song.artist = artist
        return self

    def album(self, album):
        self.song.album = album
        return self

    def art(self, art):
        self.song.art = art
        return self

    def track(self, track):
        self.song.track = track
        return self

    def yt(self, yt):
        self.song.yt = yt
        return self

    def build(self):
        if self.rf is not None:
            self.rf(self.song)
        if self.rv is not None:
            return self.rv
        return self.song

class Album:
    def __init__(self, artist=None, title=None, art=None):
        self.artist = artist
        self.title = title
        self.art = art
        self.tracks = []

    def add_track(self, song):
        if not song.artist:
            song.artist = self.artist
        if not song.album:
            song.album = self.title
        if not song.art:
            song.art = self.art

        song.track = len(self.tracks) + 1
        self.tracks.append(song)
        return self

    def __str__(self):
        return (f"Album(artist={self.artist}, title={self.title}, art={self.art}, "
                f"tracks=[{', '.join(str(track) for track in self.tracks)}])")
    
    def download(self):
        for track in self.tracks:
            track.download()

class AlbumBuilder:
    def __init__(self):
        self.album = Album()

    def artist(self, artist):
        self.album.artist = artist
        return self

    def title(self, title):
        self.album.title = title
        return self

    def art(self, art):
        self.album.art = art
        return self

    def track(self):
        return SongBuilder(lambda song: self.album.add_track(song), self)

    def build(self):
        return self.album
    
