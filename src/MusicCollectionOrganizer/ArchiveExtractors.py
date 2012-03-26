# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="gregorl"
__date__ ="$2010-08-29 19:56:43$"

import UnRAR2 as rar
import zipfile
from Logging.LoggingDecorator import Log
from Exceptions import ArchiveIncorrectPasswordException


class AllArchivesExtractor(object):

    def __init__(self, possiblePasswords, keepArchivesList):
        self.__extractors = ArchiveExtractor.GetAllArchiveExtractors()
        self.__possiblePasswords = possiblePasswords
        self.__failedToExtract = keepArchivesList

    def Extract(self, archivePath, destination):
        archiveType = archivePath.split(".")[-1]
        
        print "Extracting %s" % archivePath
        try:
            self.__extractors[archiveType].Extract(archivePath, destination)
        except ArchiveIncorrectPasswordException:
            archiveExtracted = False
            for password in self.__possiblePasswords:
                try:
                    self.__extractors[archiveType].Extract(archivePath, destination, password=password)
                    archiveExtracted = True
                    break
                except:
                    continue
            
            if not archiveExtracted:
                self.__failedToExtract.append(archivePath)
                print "IncorrectArchivePassword: %s" % archivePath

class ArchiveExtractor(object):

    SupportedFileExtension = None

    def Extract(self, archivePath, destination, password=None):
        raise NotImplementedError()

    @classmethod
    def GetAllArchiveExtractors(cls):
        return dict([ (subcls.SupportedFileExtension, subcls()) for subcls in cls.__subclasses__() ])


class RarArchiveExtractor(ArchiveExtractor):

    SupportedFileExtension = "rar"

    def Extract(self, archivePath, destination=".", password=None):
        try:
            archive = rar.RarFile(archivePath, password=password)
            if password:
                archive.extract(path=destination)
            else:
                archive.extract(path=destination)
        except rar.rar_exceptions.IncorrectRARPassword:
            raise ArchiveIncorrectPasswordException()

class ZipArchiveExtractor(ArchiveExtractor):

    SupportedFileExtension = "zip"

    def Extract(self, archivePath, destination=".", password=None):
        archive = zipfile.ZipFile(archivePath)
        
        try:
            if password:
                archive.extractall(path=destination, pwd=password)
            else:
                archive.extractall(path=destination)
        except:
            raise ArchiveIncorrectPasswordException()

