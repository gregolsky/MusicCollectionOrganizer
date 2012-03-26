# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="gregorl"
__date__ ="$2010-08-29 17:32:53$"

class MusicCollectionOrganizerException(Exception):
    pass

class MissingTagInfoException(MusicCollectionOrganizerException):
    pass

class ArchiveIncorrectPasswordException(MusicCollectionOrganizerException):
    pass

class AlbumCoverNotFoundException(Exception):
    pass