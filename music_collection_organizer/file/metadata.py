
class FileCollectionPropertiesFormatParser(object):

    def __init__(self):
        self.__collectionProperties = None
        self.__collectionPropertiesFormats = None

    def Feed(self, collectionProperties=None, collectionPropertiesFormats=None):
        if not collectionProperties or not collectionPropertiesFormats:
            raise ValueError()
        self.__collectionProperties = collectionProperties
        self.__collectionPropertiesFormats = collectionPropertiesFormats

    def GetFilePropertiesFormats(self):
        result = []
        for index, format in enumerate(self.__collectionPropertiesFormats):
            result.append([])
            properties = []
            for property in self.__collectionProperties:
                 if property in format:
                     properties.append(property)

            result[index] = FilePropertyFormat(properties=tuple(properties), format=format)

class FilePropertiesExtractor(object):

    def extractPropertiesOf(self, file):
        return None

class FileProperties(object):

    def __init__(self, **kwargs):
        self.__dict__ = kwargs

    def IsSimilar(self, other):
        pass
