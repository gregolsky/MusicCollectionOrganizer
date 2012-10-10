
import unittest
from music.archive import *

class  ArchiveInformationRetrieversTests(unittest.TestCase):
    def setUp(self):
        self.tested = AllArchivesInformationRetriever([], [])
    

    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    def testGetFilesList(self):
        assert self.tested.GetListOfFiles("tests/testdata/a.zip")
        assert self.tested.GetListOfFiles('tests/testdata/b.rar')

if __name__ == '__main__':
    unittest.main()

