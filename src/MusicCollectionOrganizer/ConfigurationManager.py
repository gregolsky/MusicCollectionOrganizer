# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="gregorl"
__date__ ="$2010-08-20 15:36:54$"

import ApplicationAbstractions.ConfigurationManager as app
from TagInfoProvider.TagInfoProvider import TagInfo
from getpass import getpass
import os
import pylast

class ConfigurationManager(app.ConfigurationManager):

    OrganizationStructure = "OrganizationStructure"
    CollectionInformation = "CollectionInformation"
    ArchivesInfo = "ArchivesInfo"
    LastFm = "LastFm"
    __ConfigurationSections = ( OrganizationStructure, CollectionInformation, ArchivesInfo, LastFm )

    def __init__(self, appname):
        app.ConfigurationManager.__init__(self, appname)
        
        try:
            self.GetCollectionDirectory()
            self.GetPossiblePasswords()
            self.GetCollectionPropertiesFormats()
            self.GetLastFmCredentials()
        except:
            self.__InitializeFormats()
            self.__InitializeDirectoryInfo()
            self.__InitializeArchivesInfo()
            self.__InitializeLastFmCredentials()

    def __InitializeLastFmCredentials(self):

        user = raw_input("LastFm Login: ")
        passwordHash = pylast.md5(getpass("LastFm Password: "))
        self.SetValue(self.LastFm, "LastFmLogin", user )
        self.SetValue(self.LastFm, "LastFmPasswordHash", passwordHash)

    def __InitializeArchivesInfo(self):
        self.SetValue(self.ArchivesInfo, "PossiblePasswords", "nodata.tv | www.mediaboom.org")

    def __InitializeDirectoryInfo(self):
        self.SetValue(self.CollectionInformation, "CollectionDirectory", "~/Organized")
        self.SetValue(self.CollectionInformation, "DownloadsDirectory", "~/Pobrane")

    def __InitializeFormats(self):
        self.SetValue(self.OrganizationStructure, "Formats", '''artist/artist - album [date]/artist - tracknumber. title''')

    def GetCollectionDirectory(self):
        return os.path.expanduser(self.GetValue(self.CollectionInformation, "CollectionDirectory"))

    def GetDownloadsDirectory(self):
        return os.path.expanduser(self.GetValue(self.CollectionInformation, "DownloadsDirectory"))

    def GetPossiblePasswords(self):
        return self.GetValue(self.ArchivesInfo, "PossiblePasswords").split(" | ")

    def GetCollectionPropertiesFormats(self):
        formats = self.GetValue(self.OrganizationStructure, "Formats")
        for key in TagInfo.TagKeys:
            formats = formats.replace(key, "%(" + key + ")s")
        propertiesFormats = formats.split('/')
        # TODO propertiesFormats.validate()
    
        return propertiesFormats

    def GetLastFmCredentials(self):
        login = self.GetValue(self.LastFm, "LastFmLogin")
        password = self.GetValue(self.LastFm, "LastFmPasswordHash")
        return (login, password)