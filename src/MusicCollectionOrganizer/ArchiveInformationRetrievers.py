
import UnRAR2 as rar
import zipfile
from MusicFileProperties import SupportedAudioFileExtensions
from Exceptions import ArchiveIncorrectPasswordException


class AllArchivesInformationRetriever(object):

    def __init__(self, possiblePasswords, failedToOpenArchives):
        self.__possiblePasswords = possiblePasswords
        self.__infoRetrievers = self.__GetAllArchiveInformationRetrievers()
        self.__failedToOpen = failedToOpenArchives

    def __GetAllArchiveInformationRetrievers(self):
        return dict([ (cls.SupportedFileExtension, cls()) for cls in ArchiveInformationRetriever.__subclasses__() ])

    def ContainsMusic(self, archivePath):
        extension = archivePath.split(".")[-1]
        infoRetriever = self.__infoRetrievers[extension]
        try:
            return infoRetriever.ContainsMusic(archivePath)
        except ArchiveIncorrectPasswordException:
            for password in self.__possiblePasswords:
                try:
                    return infoRetriever.ContainsMusic(archivePath, password)
                except:
                    continue

            self.__failedToOpen.append(archivePath)
            print "%(archivePath)s is password protected"
            return False

        except:
            self.__failedToOpen.append(archivePath)
            print "%(archivePath)s could not be opened"
            return False
    
    def __GetAppropriateInfoRetriever(self, archivePath):
        extension = archivePath.split(".")[-1]
        return self.__infoRetrievers[extension]
    
    def ContainsMusic(self, archivePath):
        infoRetriever = self.__GetAppropriateInfoRetriever(archivePath)
        try:
            return infoRetriever.ContainsMusic(archivePath)
        except ArchiveIncorrectPasswordException:
            for password in self.__possiblePasswords:
                try:
                    return infoRetriever.ContainsMusic(archivePath, password)
                except:
                    continue

            print "%(archivePath)s is password protected"
            return False

    def GetListOfFiles(self, archivePath):
        infoRetriever = self.__GetAppropriateInfoRetriever(archivePath)
        try:
            return infoRetriever.GetListOfFiles(archivePath)
        except ArchiveIncorrectPasswordException:
            for password in self.__possiblePasswords:
                try:
                    return infoRetriever.GetListOfFiles(archivePath, password)
                except:
                    continue

            print "%(archivePath)s is password protected"
            return False



class ArchiveInformationRetriever(object):

    PossiblePasswords = []

    def ContainsMusic(self, archivePath):
        raise NotImplementedError()

    def GetListOfFiles(self, archivePath, password=None):
        raise NotImplementedError()

class RarArchiveInformationRetriever(ArchiveInformationRetriever):

    SupportedFileExtension = "rar"

    def __init__(self):
        pass

    def ContainsMusic(self, archivePath, password=None):
        try:
            archive = rar.RarFile(archivePath, password=password)
        except rar.rar_exceptions.IncorrectRARPassword:
            raise ArchiveIncorrectPasswordException()
        try:        
            result = any(( any(( archiveElement.filename.endswith(extension) for extension in SupportedAudioFileExtensions)) for archiveElement in archive.infoiter() ))
        except:
            return False

        return result

    def GetListOfFiles(self, archivePath, password=None):
        try:
            archive = rar.RarFile(archivePath, password=password)
        except rar.rar_exceptions.IncorrectRARPassword:
            raise ArchiveIncorrectPasswordException()
        return ( archiveElement.filename for archiveElement in archive.infoiter() )


class ZipArchiveInformationRetriever(ArchiveInformationRetriever):

    SupportedFileExtension = "zip"

    def __init__(self):
	pass

    def ContainsMusic(self, archivePath, password=None):
        archive = zipfile.ZipFile(archivePath)
        if password:
            archive.setpassword(password)
	try:
            return any(( any(( archiveElement.filename.endswith(extension) for extension in SupportedAudioFileExtensions)) for archiveElement in archive.infolist()))
	except:
            raise ArchiveIncorrectPasswordException()

    def GetListOfFiles(self, archivePath, password=None):
        archive = zipfile.ZipFile(archivePath)
        if password:
            archive.setpassword(password)
	try:
            return ( archiveElement.filename for archiveElement in archive.infolist() )
	except:
            raise ArchiveIncorrectPasswordException()

