
import os
import sys

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






