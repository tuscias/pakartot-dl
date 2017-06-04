import json
import urllib
import urllib2


FILENAME = __file__
URL = 'https://www.pakartot.lt'
API_URL = 'https://api.pakartot.lt/'
USERNAME = 'publicUSR'
PASSWORD = 'vka3qaGHowofKcRdTeiV'


def __doRequest(url, additionalParams):
    params = {'username': USERNAME, 'password': PASSWORD, 'url': url}
    params.update(additionalParams)
    data = urllib.urlencode(params)

    return urllib2.urlopen(API_URL, data)

def getAlbumId(url):
    html = urllib2.urlopen(url).read()
    index = html.find('class="play-release" title="')
    index2 = html.find('"', index + 52)

    return html[index + 52:index2]

def getAlbumInfo(albumId):
    response = __doRequest('album', {'id': albumId})
    data = json.loads(response.read())
    return data['album']


def getAlbumTracksInfo(albumId):
    response = __doRequest('album', {'id': albumId})
    data = json.loads(response.read())
    return data['tracks']


def getAlbumTracksInfoEx(albumId):
    response = __doRequest('play', {'action': 'album', 'id': albumId})
    data = json.loads(response.read())
    return data['tracks']

def downloadTrack(trackUrl, saveLocation):
    req = urllib2.Request(trackUrl)
    req.add_header('User-Agent', 'iPhone;')
    fileContent =  urllib2.urlopen(req).read()

    with open(saveLocation, 'wb') as f:
        f.write(fileContent)

def downloadCoverArt(coverArtUrl, saveLocation):
    coverArtContent = urllib2.urlopen(coverArtUrl).read()

    with open(saveLocation, 'wb') as f:
        f.write(saveLocation)
