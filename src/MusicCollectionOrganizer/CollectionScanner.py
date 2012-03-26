# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="gregorl"
__date__ ="$2010-08-28 14:54:08$"

from FileCollectionOrganizer.FileCollectionScanner import FileCollectionScanner
import os

class MusicCollectionScanner(FileCollectionScanner):

    def GetCollectionFromDirectory(self, directory):
        collection = []
        for dirpath, dirnames, filenames in os.walk(directory):
            for fname in filenames:
                if fname.endswith(".mp3"):
                    collection.append(os.path.join(dirpath, fname))

        return collection
