#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="gregorl"
__date__ ="$2010-08-20 15:27:33$"


import sys
import traceback
import ApplicationAbstractions.Application as app

from ConfigurationManager import ConfigurationManager
from MusicCollectionOrganizer import MusicCollectionOrganizer
from MusicFilePropertiesExtractor import MusicFilePropertiesExtractor
from TagInfoProvider.TagInfoProvider import TagInfoProvider
from UnpleasantCharsCutter import UnpleasantCharactersCutter
from CollectionScanner import MusicCollectionScanner
from MusicArchiveInformationManager import MusicArchivesInformationManager
from ArchiveInformationRetrievers import AllArchivesInformationRetriever
from ArchiveExtractors import AllArchivesExtractor
from CoverDownloaders import LastFmCoverDownloader, AlbumArtOrgCoverDownloader
from ExtractedArchivesCleaner import ExtractedArchivesCleaner

class MusicCollectionOrganizerApplication(app.Application):

    def __init__(self):
        app.Application.__init__(self)

    def _ApplicationConfigurationInitialize(self):
        self.ConfigurationManager = ConfigurationManager(self.__class__.__name__)

    def _ApplicationInit(self):
        self.__musicCollectionScanner = MusicCollectionScanner()

        possiblePasswords = self.ConfigurationManager.GetPossiblePasswords()
        self.__keepArchivesList = []
        self.__archiveInformationRetriever = AllArchivesInformationRetriever(possiblePasswords, self.__keepArchivesList)
        self.__musicArchivesInformationManager = MusicArchivesInformationManager(self.__archiveInformationRetriever)
        self.__archiveExtractor = AllArchivesExtractor(possiblePasswords, self.__keepArchivesList)
        self.__extractedArchivesCleaner = ExtractedArchivesCleaner(self.__archiveInformationRetriever)

        tagInfoProvider = TagInfoProvider(UnpleasantCharactersCutter())
        self.__propertiesExtractor = propertiesExtractor = MusicFilePropertiesExtractor(tagInfoProvider, self.__keepArchivesList)
        formats = self.ConfigurationManager.GetCollectionPropertiesFormats()

        lastfmCredentials = self.ConfigurationManager.GetLastFmCredentials()
        coverDownloaders = [ AlbumArtOrgCoverDownloader(), LastFmCoverDownloader(lastfmCredentials) ]
        self.__organizer = MusicCollectionOrganizer(formats, propertiesExtractor, coverDownloaders)

    def _ApplicationStart(self):

        foundArchives = self.__musicArchivesInformationManager.RetrieveArchives(sys.argv[1])

        for archive in foundArchives.keys():
            self.__archiveExtractor.Extract(archive, sys.argv[1])

        self.__propertiesExtractor.setArchivesInfoForMaintenance(foundArchives)

        collection = self.__musicCollectionScanner.GetCollectionFromPath(sys.argv[1])
        collectionDir = self.ConfigurationManager.GetCollectionDirectory()
        self.__organizer.Organize(collection, collectionDir)

        self.__extractedArchivesCleaner.CleanUp(sys.argv[1], foundArchives, self.__keepArchivesList)

    def _ApplicationError(self, error):
        traceback.print_exc(file=sys.stderr)

    def _ApplicationEnd(self):
        #clean up
        pass

    def _ApplicationOnErrorDeinitialize(self):
        #clean up
        pass


if __name__ == "__main__":
    MusicCollectionOrganizerApplication().ApplicationMain()