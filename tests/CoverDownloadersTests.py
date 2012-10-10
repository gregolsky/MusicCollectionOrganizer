# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="gregorl"
__date__ ="$2010-09-01 18:25:06$"

import unittest
from music.cover import *

class CoverDownloadersTests(unittest.TestCase):

    def setUp(self):
        pass

    def testRymCoverDownloader(self):
        tested = RateYourMusicCoverDownloader()
        #tested.DownloadCoverFor('Tool', 'Lateralus','.')

    def tearDown(self):
        pass
