# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="gregorl"
__date__ ="$2010-08-28 15:34:11$"

import unittest
from music.metadata import MusicFileProperties

class MusicFilePropertiesTests(unittest.TestCase):

    def testIsSimilar(self):
        tested1 = MusicFileProperties(artist="a", album='b', date='2010',title='asdf',tracknumber='2')
        tested2 = MusicFileProperties(artist="a", album='b', date='2010',title='asdf2',tracknumber='4')
        tested1.IsSimilar(tested2)
