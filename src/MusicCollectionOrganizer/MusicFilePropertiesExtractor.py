# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="gregorl"
__date__ ="$2010-08-20 16:15:16$"

from FileCollectionOrganizer.FilePropertiesExtractor import FilePropertiesExtractor
from MusicFileProperties import MusicFileProperties
from Caching.MemoizeDecorator import Memoized
import TagInfoProvider.MissingTagInfoException as tagException

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
            return MusicFileProperties(artist= tagInfo.Artist,
                                    album= tagInfo.Album,
                                    title= tagInfo.Title,
                                    date= tagInfo.Year,
                                    tracknumber= tagInfo.TrackNumber)
        except tagException.MissingTagInfoException as exc:
            if file in self.__archivesListOfFiles:
                self.__keepArchivesList.append(self.__archivesListOfFiles[file])

            print str(exc)
        
