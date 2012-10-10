import math
import os
import urllib
import pylast
import urllib2
import sgmllib
from lxml.html import fromstring
import music.common

#from .common import DataTransferObject

class CoverDownloader(object):

    def DownloadCoverFor(self, artist, album, destination):
        pass

    @staticmethod
    def IsAlbumNameSimilar(albumName, webAlbumName):
        if albumName and webAlbumName:
            webAlbumNameWords = [ n.encode('utf-8') for n in webAlbumName.lower().split() ]
            albumNameWords = albumName.lower().split()
            subLenAlbumNames = int(math.fabs(len(albumNameWords) - len(webAlbumNameWords)))
            return sum([ 1 for word in albumNameWords if word in webAlbumNameWords ]) >= 1 and subLenAlbumNames <= 2
        
        return False

class RateYourMusicCoverDownloader(object):

    Site = "http://rateyourmusic.com/"
    UnusualCharacters = r""",'"~.'`:;\/?][)(+- &^%$#@!"""

    class RateYourMusicUrlOpener(urllib.FancyURLopener):
        version = "MusicCollectionOrganizer"

    def __init__(self):
        urllib._urlopener = self.RateYourMusicUrlOpener()

    def GetUrlArtistName(self, artistName):
        return "".join([ character if character not in self.UnusualCharacters else "_" for character in artistName.lower() ])

    def DownloadCoverFor(self, artist, album, destination):
        artistPageUrl = self.Site + "artist/" + self.GetUrlArtistName(artist) + '/'
        artistPage = urllib.urlopen(artistPageUrl).read()
        artistPageParser = self.RateYourMusicArtistPageHtmlParser()
        artistPageParser.feed(artistPage)

    class RateYourMusicArtistPageHtmlParser(sgmllib.SGMLParser):

        class Anchor(music.common.DataTransferObject):
            pass

        def __init__(self):
            sgmllib.SGMLParser.__init__(self)
            self.__anchors = []
            self.__IsProcessingAnchor = False
            self.__currentAnchor = None
            self.__IsProcessingSpan = False
            self.__IsDiscography = False

        def start_span(self, attributes):
            self.__IsProcessingSpan = True

        def end_span(self):
            self.__IsProcessingSpan = False

        def start_a(self, attributes):
            if self.__IsDiscography:
                self.__IsProcessingAnchor = True
                self.__currentAnchor = self.Anchor(data=None, link=attributes[0])

        def handle_data(self, data):
            if self.__IsProcessingAnchor:
                self.__currentAnchor.data = data
            elif self.__IsProcessingSpan:
                if data.strip() == 'discography':
                    self.__IsDiscography = True

        def end_a(self):
            if self.__IsDiscography:
                self.__IsProcessingAnchor = False
                self.__anchors.append(self.__currentAnchor)

        def GetAnchors(self):
            print self.__anchors
            return self.__anchors


class AlbumArtOrgCoverDownloader(CoverDownloader):

    Url = 'http://www.albumart.org/index.php'

    def DownloadCoverFor(self, artist, album, destination):

        data = {}
        data["srchkey"] = "%(artist)s %(album)s" % locals()
        data["itempage"] = 1
        data["newsearch"] = 1
        data["searchindex"] = "Music"

        try:
            sock = urllib2.urlopen(self.Url+"?"+urllib.urlencode(data))
            content = sock.read()
            anchors = fromstring(content).cssselect("a.thickbox")
            link = anchors[0].get('href')
            urllib.urlretrieve(link, os.path.join(destination, 'folder.' + link.split('/')[-1].split('.')[-1]))
        except:
            raise music.common.AlbumCoverNotFoundException("No album cover on AlbumArt.org for %(artist)s - %(album)s" % locals())


class LastFmCoverDownloader(CoverDownloader):

    API_KEY = "c24c87da37668d0147a16e2e44bba24a"
    API_SECRET = "77df19816a250e40d0d78fcb870318a9"

    def __init__(self, lastfmCredentials):
        username, password = lastfmCredentials
        self.__network = self.__ConnectToLastFm(username, password)

    def DownloadCoverFor(self, artist, album, destination):
        try:
            albums = [ topalbum[0].get_cover_image() for topalbum in self.__network.get_artist(artist).get_top_albums() if CoverDownloader.IsAlbumNameSimilar(album, topalbum[0].get_title()) ]
            if albums:
                urllib.urlretrieve(albums[0], os.path.join(destination,'folder.' + albums[0].split('/')[-1].split('.')[-1]))
        except:
            raise music.common.AlbumCoverNotFoundException("No album cover on Last.Fm for %(artist)s - %(album)s" % locals())

    def __ConnectToLastFm(self, username, password):
        return pylast.get_lastfm_network(api_key = self.API_KEY, api_secret = self.API_SECRET, username = username, password_hash = password)

