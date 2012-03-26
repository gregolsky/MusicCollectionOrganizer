import os.path

__author__="gregorl"
__date__ ="$2010-09-02 18:20:11$"

import os
import shutil

from FileCollectionOrganizer.FileMover import FileMover

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
                    
