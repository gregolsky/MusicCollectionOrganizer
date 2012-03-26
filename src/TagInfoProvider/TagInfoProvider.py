
from mutagen.easyid3 import EasyID3
from MissingTagInfoException import MissingTagInfoException
import re

class TagInfo(object):

    ArtistKey = "artist"
    TitleKey = "title"
    TrackNrKey = "tracknumber"
    AlbumKey = "album"
    DateKey = "date"
    TagKeys = [ ArtistKey, AlbumKey, TitleKey, DateKey, TrackNrKey ]

    def __init__(self, artist, album, title, tracknr, date):
        self.__artist = artist
        self.__album = album
        self.__title = title
        self.__tracknr = tracknr
        self.__date = date

    def get_artist(self):
        return self.__artist
    
    def get_album(self):
        return self.__album
    
    def get_title(self):
        return self.__title
    
    def get_tracknr(self):
        return self.__tracknr
    
    def get_date(self):
        return self.__date
        
    Artist = property(get_artist, None, None, None)
    Album = property(get_album, None, None, None)
    Title = property(get_title, None, None, None)
    TrackNumber = property(get_tracknr, None, None, None)
    Year = property(get_date, None, None, None)

class TagInfoProvider(object):

    def __init__(self, unpleasantCharactersCutter):
        self.__UnpleasantCharactersCutter = unpleasantCharactersCutter 

    def getTagInfoForFile(self, filename):

        tags = None
        try:
            tags = EasyID3(filename)
        except:
            raise MissingTagInfoException("No ID3 header in %s"%filename)

        try:
            artist = self.__UnpleasantCharactersCutter.cutUnpleasantCharacters(tags[TagInfo.ArtistKey][0]).title()
            tracknr = int(tags[TagInfo.TrackNrKey][0].split("/")[0])
            title = self.__UnpleasantCharactersCutter.cutUnpleasantCharacters(tags[TagInfo.TitleKey][0]).title()
            date = re.search(r'''.*([0-9]{4}).*''', tags[TagInfo.DateKey][0]).groups(1)[0]
            tracknumber = '0' +  self.__UnpleasantCharactersCutter.cutUnpleasantCharacters(str(tracknr)) if tracknr<10 else str(tracknr)
            album = self.__UnpleasantCharactersCutter.cutUnpleasantCharacters(tags[TagInfo.AlbumKey][0]).title()
            
            return TagInfo(artist, album, title, tracknumber, date)

        except Exception:
            raise MissingTagInfoException("No artist, title or tracknumber tag in %s"%filename)
