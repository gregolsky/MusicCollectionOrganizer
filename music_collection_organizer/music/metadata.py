import re
from caching import Memoized
from mutagen.easyid3 import EasyID3
from file.metadata import FileProperties, FilePropertiesExtractor
import music.common

class UnpleasantCharactersCutter(object):

    UnpleasantCharacters = r""",'"~.'`:;\/?][)("""

    def cutUnpleasantCharacters(self, s):
        return "".join([c for c in s.strip() if c not in self.UnpleasantCharacters])


class MetaData(object):

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


class MusicMetadataProvider(object):

    def __init__(self, unpleasantCharactersCutter):
        self.__UnpleasantCharactersCutter = unpleasantCharactersCutter 

    def getTagInfoForFile(self, filename):

        tags = None
        try:
            tags = EasyID3(filename)
        except:
            raise music.common.MissingTagInfoException("No ID3 header in %s"%filename)

        try:
            artist = self.__UnpleasantCharactersCutter.cutUnpleasantCharacters(tags[MetaData.ArtistKey][0]).title()
            tracknr = int(tags[MetaData.TrackNrKey][0].split("/")[0])
            title = self.__UnpleasantCharactersCutter.cutUnpleasantCharacters(tags[MetaData.TitleKey][0]).title()
            date = re.search(r'''.*([0-9]{4}).*''', tags[MetaData.DateKey][0]).groups(1)[0]
            tracknumber = '0' +  self.__UnpleasantCharactersCutter.cutUnpleasantCharacters(str(tracknr)) if tracknr<10 else str(tracknr)
            album = self.__UnpleasantCharactersCutter.cutUnpleasantCharacters(tags[MetaData.AlbumKey][0]).title()
            
            return MetaData(artist, album, title, tracknumber, date)

        except Exception:
            raise music.common.MissingTagInfoException("No artist, title or tracknumber tag in %s"%filename)


class MusicFilePropertiesExtractor(FilePropertiesExtractor):

    def __init__(self, tagInfoProvider, keepArchivesList):
        self.__tagInfoProvider = tagInfoProvider
        self.__archivesListOfFiles = {}
        self.__keepArchivesList = keepArchivesList
        
    def setArchivesInfoForMaintenance(self, archives):
        for archivePath,flist in archives.iteritems():
            for f in flist:
                self.__archivesListOfFiles[f] = archivePath

    @Memoized
    def extractPropertiesOf(self, file):
        try:
            tagInfo = self.__tagInfoProvider.getTagInfoForFile(file)
            return music.metadata.MusicFileProperties(artist= tagInfo.Artist,
                                    album= tagInfo.Album,
                                    title= tagInfo.Title,
                                    date= tagInfo.Year,
                                    tracknumber= tagInfo.TrackNumber)
        except music.common.MissingTagInfoException as exc:
            if file in self.__archivesListOfFiles:
                self.__keepArchivesList.append(self.__archivesListOfFiles[file])

            print str(exc)

SupportedAudioFileExtensions = [ ".mp3", ".flac", "ogg" ]

class MusicFileProperties(FileProperties):

    def __init__(self, **kwargs):
        for k in MetaData.TagKeys:
            if not kwargs.has_key(k):
                raise Exception("MusicFileProperties ctor didn't receive enough information")

        FileProperties.__init__(self, **kwargs)

    def IsSimilar(self, other):
        for k in ( k for k in MetaData.TagKeys if k not in [ MetaData.TrackNrKey, MetaData.TitleKey]):
            if self.__dict__[k] != other.__dict__[k]:
                return False

        return True

