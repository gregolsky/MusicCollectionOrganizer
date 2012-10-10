import sys
import UnRAR2 as rar
import zipfile
import os.path
import shutil
from music.metadata import SupportedAudioFileExtensions
from file.utils import FileMover
import music.common

class MusicArchivesInformationManager(object):

    __RarFileExtension = "rar"
    __ZipFileExtension = "zip"
    __SevenZipFileExtension = "7z"

    SupportedExtensions = [ __RarFileExtension, __ZipFileExtension, __SevenZipFileExtension ]

    def __init__(self, archiveInformationRetriever):
        self.__archiveInformationRetriever = archiveInformationRetriever

    def RetrieveArchives(self, path):

        results = {}
        for dirpath, dirnames, filenames in os.walk(path):
            archives = ( os.path.join(dirpath, fname) for fname in filenames if any([ fname.endswith(".%s" % extension) for extension in self.SupportedExtensions ]) )
            musicArchives = dict([ (archivePath, self.__archiveInformationRetriever.GetListOfFiles(archivePath))  for archivePath in archives if self.__archiveInformationRetriever.ContainsMusic(archivePath)])

            for path, flist in musicArchives.iteritems():
                results[path] = [ os.path.join(sys.argv[1], fpath[1:] if fpath[0] == "*" else fpath ) for fpath in flist  ]
        return results


class ExtractedArchivesCleaner(object):

    def __init__(self, archiveInfoRetriever):
        self.__archiveInformationRetriever = archiveInfoRetriever

    def CleanUp(self, unpackLocation, archives, keepArchivesList):
        archivesFiles = []
        for arc in archives:
            for file in self.__archiveInformationRetriever.GetListOfFiles(arc):
                archivesFiles.append(file)

        for file in archivesFiles:
            filePath = os.path.join(unpackLocation, file if file[0] != '*' else file[1:])
            if os.path.exists(filePath):
                if os.path.isfile(filePath):
                    os.remove(filePath)
                elif os.path.isdir(filePath):
                    shutil.rmtree(filePath)

        manualMaintenanceNeededDirectory = os.path.join(unpackLocation, 'ManualMaintenanceNeeded')
        if not os.path.exists(manualMaintenanceNeededDirectory):
            os.mkdir(manualMaintenanceNeededDirectory)

        for arc in archives:
            if arc in keepArchivesList:
                FileMover.MoveFile(arc, os.path.join(manualMaintenanceNeededDirectory, os.path.split(arc)[1]))
            else:
                try:
                    os.unlink(arc)
                except OSError as oserr:
                    print oserr

class ArchiveInformationRetriever(object):

    PossiblePasswords = []

    def ContainsMusic(self, archivePath):
        raise NotImplementedError()

    def GetListOfFiles(self, archivePath, password=None):
        raise NotImplementedError()

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
            raise music.common.ArchiveIncorrectPasswordException()

    def GetListOfFiles(self, archivePath, password=None):
        archive = zipfile.ZipFile(archivePath)
        if password:
            archive.setpassword(password)
	try:
            return ( archiveElement.filename for archiveElement in archive.infolist() )
	except:
            raise music.common.ArchiveIncorrectPasswordException()

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
        except music.common.ArchiveIncorrectPasswordException:
            for password in self.__possiblePasswords:
                try:
                    return infoRetriever.ContainsMusic(archivePath, password)
                except:
                    continue

            self.__failedToOpen.append(archivePath)
            print "%(archivePath)s is password protected" % locals()
            return False

        except:
            self.__failedToOpen.append(archivePath)
            print "%(archivePath)s could not be opened" % locals()
            return False
    
    def __GetAppropriateInfoRetriever(self, archivePath):
        extension = archivePath.split(".")[-1]
        return self.__infoRetrievers[extension]

    def GetListOfFiles(self, archivePath):
        infoRetriever = self.__GetAppropriateInfoRetriever(archivePath)
        try:
            return infoRetriever.GetListOfFiles(archivePath)
        except music.common.ArchiveIncorrectPasswordException:
            for password in self.__possiblePasswords:
                try:
                    return infoRetriever.GetListOfFiles(archivePath, password)
                except:
                    continue

            print "%(archivePath)s is password protected" % locals()
            return False

class ArchiveExtractor(object):

    SupportedFileExtension = None

    def Extract(self, archivePath, destination, password=None):
        raise NotImplementedError()

    @classmethod
    def GetAllArchiveExtractors(cls):
        return dict([ (subcls.SupportedFileExtension, subcls()) for subcls in cls.__subclasses__() ])

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
            raise music.common.ArchiveIncorrectPasswordException()


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
            raise music.common.ArchiveIncorrectPasswordException()

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
        except music.common.ArchiveIncorrectPasswordException:
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
