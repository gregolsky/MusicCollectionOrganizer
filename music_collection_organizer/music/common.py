class DataTransferObject(object):

    def __init__(self, **kwargs):
        self.__dict__ = kwargs
class AlbumCoverNotFoundException(Exception):
    pass
class MusicCollectionOrganizerException(Exception):
    pass

class MissingTagInfoException(MusicCollectionOrganizerException):
	pass

class ArchiveIncorrectPasswordException(MusicCollectionOrganizerException):
    pass
