import TagInfoProvider
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="gregorl"
__date__ ="$2010-08-20 16:09:49$"

from TagInfoProvider.TagInfoProvider import TagInfo
from FileCollectionOrganizer.FileProperties import FileProperties

SupportedAudioFileExtensions = [ ".mp3", ".flac", "ogg" ]

class MusicFileProperties(FileProperties):

    def __init__(self, **kwargs):
        for k in TagInfo.TagKeys:
            if not kwargs.has_key(k):
                raise Exception("MusicFileProperties ctor didn't receive enough information")

        FileProperties.__init__(self, **kwargs)

    def IsSimilar(self, other):
        for k in ( k for k in TagInfo.TagKeys if k not in [ TagInfo.TrackNrKey, TagInfo.TitleKey]):
            if self.__dict__[k] != other.__dict__[k]:
                return False

        return True