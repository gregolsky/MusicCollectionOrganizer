# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="gregorl"
__date__ ="$2010-08-28 13:15:48$"

import unittest
from music.organize import ConfigurationManager

class MusicCollectionOrganizerConfigurationManagerTests(unittest.TestCase):

    def setUp(self):
        self.tested = ConfigurationManager("musicCollectionOrganizerTest")

    def testInit(self):
        with self.tested:
            assert self.tested != None
            assert self.tested.GetSection("OrganizationStructure") != None
            print self.tested.GetValue("OrganizationStructure", "Formats")
            assert self.tested.GetValue("OrganizationStructure", "Formats") == '''artist/artist - album [date]/artist - tracknumber. title'''

    def tearDown(self):
        pass
