import os.path

__author__="gregorl"
__date__ ="$2010-08-20 16:06:04$"

import os
from FileMover import FileMover

class FileCollectionOrganizer(object):

    def __init__(self, collectionPropertiesFormats, filePropertiesExtractor):
        self.__collectionPropertiesFormats = collectionPropertiesFormats
        self.__filePropertiesExtractor = filePropertiesExtractor
        self.__afterOrganizationActions = []

    def AddAfterOrganizationAction(self, f):
        self.__afterOrganizationActions.append(f)

    def Organize(self, collection, collectionDirectory):

        if not os.path.exists(collectionDirectory):
            os.mkdir(collectionDirectory)

        elementsProperties = dict([ (e, self.__filePropertiesExtractor.extractPropertiesOf(e)) for e in collection if self.__filePropertiesExtractor.extractPropertiesOf(e) != None ])
        organized = []
        for element in collection:
            if element not in organized:
                similarElements = [ other for other in collection if elementsProperties.has_key(element) and elementsProperties.has_key(other) and elementsProperties[element].IsSimilar(elementsProperties[other]) ]
                localVariables = locals()
                similarElementsDirectory = None
                
                for chosenElement in similarElements:
                    for key, value in elementsProperties[chosenElement].__dict__.iteritems():
                        localVariables[key] = value

                    formattedDirectoriesNames = [ collectionDirectory ]
                    for formatString in self.__collectionPropertiesFormats[:-1]:
                        formattedDirectoriesNames.append(formatString % locals())

                    similarElementsDirectory = os.path.join(*formattedDirectoriesNames)
                    if not os.path.exists(similarElementsDirectory):
                        os.makedirs(similarElementsDirectory)
                    FileMover.MoveFile(file=chosenElement, destination=os.path.join(similarElementsDirectory, self.__collectionPropertiesFormats[-1] % locals() + '.' + chosenElement.split('.')[-1]))
                    organized.append(chosenElement)

                self.__ApplyActionsOnSimilarElements(similarElements, elementsProperties, similarElementsDirectory)

    def __ApplyActionsOnSimilarElements(self, similarElements, elementsProperties,similarElementsDirectory):
        for action in self.__afterOrganizationActions:
            action(similarElements, elementsProperties, similarElementsDirectory)
