# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="gregorl"
__date__ ="$2010-08-20 16:02:05$"

from FileCollectionOrganizer.FileCollectionOrganizer import FileCollectionOrganizer
from Exceptions import AlbumCoverNotFoundException

class MusicCollectionOrganizer(FileCollectionOrganizer):

    def __init__(self, collectionPropertiesFormats, filePropertiesExtractor, coverDownloaders):
        FileCollectionOrganizer.__init__(self, collectionPropertiesFormats, filePropertiesExtractor)
        self.__coverDownloaders = coverDownloaders
        self.AddAfterOrganizationAction(self.DownloadCovers)


    def DownloadCovers(self, similarElements, elementsProperties, similarElementsDirectory):
        if similarElements:
            element = elementsProperties[similarElements[0]]
            artist, album = element.artist, element.album
            print "Getting album cover for %(artist)s - %(album)s" % locals()
            for coverDownloader in self.__coverDownloaders:
                try:
                    coverDownloader.DownloadCoverFor(artist, album, similarElementsDirectory)
                    break
                except AlbumCoverNotFoundException:
                    continue
