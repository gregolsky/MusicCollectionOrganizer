# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="gregorl"
__date__ ="$2010-08-28 12:55:04$"

import unittest
import os
import shutil
from FileCollectionOrganizer.FileMover import FileMover

class FileMoverTests(unittest.TestCase):

    def setUp(self):
        self.testDir = "testFileMoverDir"
        self.testFile = "testFile.file"
        os.mkdir(self.testDir)
        os.system("touch %s" % self.testFile)

    def testMoveFile1(self):
        FileMover.MoveFile(self.testFile, self.testDir)
        os.path.exists(os.path.join(self.testDir, self.testFile))

    def testMoveFile2(self):
        FileMover.MoveFile(self.testFile, os.path.join(self.testDir, "dupa.file"))
        os.path.exists(os.path.join(self.testDir, self.testFile))

    def tearDown(self):
        shutil.rmtree(self.testDir)