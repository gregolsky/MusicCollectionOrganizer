
__author__="gregorl"
__date__ ="$2010-08-28 14:35:18$"

import os

class FileCollectionScanner(object):

    def __init__(self):
        pass

    def GetCollectionFromPath(self, path):
        return self.GetCollectionFromDirectory(path)

    def GetCollectionFromDirectory(self, directory):
        collection = []
        for dirpath, dirnames, filenames in os.walk(directory):
            for fname in filenames:
                collection.append(os.path.join(dirpath, fname))

        return collection
