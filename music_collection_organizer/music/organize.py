import os
import framework as app
import pylast
import sys
import traceback
from getpass import getpass
from file.organize import FileCollectionScanner, FileCollectionOrganizer
from music.cover import LastFmCoverDownloader, AlbumArtOrgCoverDownloader
from music.archive import ExtractedArchivesCleaner, MusicArchivesInformationManager, AllArchivesInformationRetriever, AllArchivesExtractor
from music.common import AlbumCoverNotFoundException
from music.metadata import MusicFilePropertiesExtractor, UnpleasantCharactersCutter, MetaData, MusicMetadataProvider

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

        tagInfoProvider = MusicMetadataProvider(UnpleasantCharactersCutter())
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


class ConfigurationManager(app.ConfigurationManager):

    OrganizationStructure = "OrganizationStructure"
    CollectionInformation = "CollectionInformation"
    ArchivesInfo = "ArchivesInfo"
    LastFm = "LastFm"
    __ConfigurationSections = ( OrganizationStructure, CollectionInformation, ArchivesInfo, LastFm )

    def __init__(self, appname):
        app.ConfigurationManager.__init__(self, appname)
        
        try:
            self.GetCollectionDirectory()
            self.GetPossiblePasswords()
            self.GetCollectionPropertiesFormats()
            self.GetLastFmCredentials()
        except:
            self.__InitializeFormats()
            self.__InitializeDirectoryInfo()
            self.__InitializeArchivesInfo()
            self.__InitializeLastFmCredentials()

    def __InitializeLastFmCredentials(self):

        user = raw_input("LastFm Login: ")
        passwordHash = pylast.md5(getpass("LastFm Password: "))
        self.SetValue(self.LastFm, "LastFmLogin", user )
        self.SetValue(self.LastFm, "LastFmPasswordHash", passwordHash)

    def __InitializeArchivesInfo(self):
        self.SetValue(self.ArchivesInfo, "PossiblePasswords", "nodata.tv | www.mediaboom.org")

    def __InitializeDirectoryInfo(self):
        self.SetValue(self.CollectionInformation, "CollectionDirectory", "~/Organized")
        self.SetValue(self.CollectionInformation, "DownloadsDirectory", "~/Pobrane")

    def __InitializeFormats(self):
        self.SetValue(self.OrganizationStructure, "Formats", '''artist/artist - album [date]/artist - tracknumber. title''')

    def GetCollectionDirectory(self):
        return os.path.expanduser(self.GetValue(self.CollectionInformation, "CollectionDirectory"))

    def GetDownloadsDirectory(self):
        return os.path.expanduser(self.GetValue(self.CollectionInformation, "DownloadsDirectory"))

    def GetPossiblePasswords(self):
        return self.GetValue(self.ArchivesInfo, "PossiblePasswords").split(" | ")

    def GetCollectionPropertiesFormats(self):
        formats = self.GetValue(self.OrganizationStructure, "Formats")
        for key in MetaData.TagKeys:
            formats = formats.replace(key, "%(" + key + ")s")
        propertiesFormats = formats.split('/')
        # TODO propertiesFormats.validate()
    
        return propertiesFormats

    def GetLastFmCredentials(self):
        login = self.GetValue(self.LastFm, "LastFmLogin")
        password = self.GetValue(self.LastFm, "LastFmPasswordHash")
        return (login, password)


class MusicCollectionScanner(FileCollectionScanner):

    def GetCollectionFromDirectory(self, directory):
        collection = []
        for dirpath, dirnames, filenames in os.walk(directory):
            for fname in filenames:
                if fname.endswith(".mp3"):
                    collection.append(os.path.join(dirpath, fname))

        return collection


class MusicCollectionOrganizer(FileCollectionOrganizer):

    def __init__(self, collectionPropertiesFormats, filePropertiesExtractor, coverDownloaders):
        FileCollectionOrganizer.__init__(self, collectionPropertiesFormats, filePropertiesExtractor)
        self.__coverDownloaders = coverDownloaders
        self.AddAfterOrganizationAction(self.DownloadCovers)


    def DownloadCovers(self, similarElements, elementsProperties, similarElementsDirectory):
        if similarElements:
            element = elementsProperties[similarElements[0]]
            artist, album = element.artist.encode('utf-8'), element.album.encode('utf-8')
            
            print "Getting album cover for %(artist)s - %(album)s" % locals()
            
            for coverDownloader in self.__coverDownloaders:
                try:
                    coverDownloader.DownloadCoverFor(artist, album, similarElementsDirectory)
                    break
                except AlbumCoverNotFoundException:
                    continue
