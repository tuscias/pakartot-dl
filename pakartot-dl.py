import os
import sys
import json
import getopt
import urllib
import urllib2
from slugify import slugify

FILENAME = __file__
URL = 'https://www.pakartot.lt'
API_URL = 'https://api.pakartot.lt/'
USERNAME = 'publicUSR'
PASSWORD = 'vka3qaGHowofKcRdTeiV'


def doRequest(url, additionalParams):
    params = {'username': USERNAME, 'password': PASSWORD, 'url': url}
    params.update(additionalParams)
    data = urllib.urlencode(params)

    return urllib2.urlopen(API_URL, data)

def getAlbumId(url):
    html = urllib2.urlopen(url).read()
    index = html.find('class="play-release" title="')
    index2 = html.find('"', index + 52)

    return html[index + 52:index2]

def getAlbum(albumUrl):
    albumId = getAlbumId(albumUrl)
    response = doRequest('album', {'id': albumId})
    data = json.loads(response.read())
    return data['album']


def getAlbumTracks(albumUrl):
    albumId = getAlbumId()
    response = doRequest('album', {'id': albumId})
    data = json.loads(response.read())
    return data['tracks']


def downloadAlbum(album, saveFolder, createAlbumFolder=False):
    response = doRequest('play', {'action': 'album', 'id': album['album_id']})
    data = json.loads(response.read())

    if createAlbumFolder:
        saveFolder = os.path.join(saveFolder, slugify(album['album_name']))

    if not os.path.exists(saveFolder):
        os.makedirs(saveFolder)

    for i, track in enumerate(data['tracks']):
        trackUrl = track['filename']
        title = slugify(track['title'])
        fileName = "%s.%s.mp3" % (i+1, title)

        saveLocation = os.path.join(saveFolder, fileName)

        print 'Downloading "%s"...' % title,

        req = urllib2.Request(trackUrl)
        req.add_header('User-Agent', 'iPhone;')
        fileContent = urllib2.urlopen(req).read()

        print ' to "%s"' % saveLocation
        with open(saveLocation, 'wb') as f:
            f.write(fileContent)


def main(argv):
    albumUrl = ''
    urlFilePath = ''
    saveFolder = ''
    createAlbumFolder = False
    albumUrls = []

    try:
        opts, args = getopt.getopt(argv, "hu:f:s:c", ["album-url=", "url-file=", "save-folder="])
    except getopt.GetoptError:
        print '%s -u <albumUrl> -s <saveFolder>' % FILENAME
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print '%s -u <albumUrl> -s <saveFolder> [-c]' % FILENAME
            sys.exit()

        elif opt in ("-u", "--album-url"):
            albumUrl = arg
        elif opt in ("-f", "--url-file"):
            urlFilePath = arg
        elif opt in ("-s", "--save-folder"):
            saveFolder = arg
        elif opt == "-c":
            createAlbumFolder = True

    if not createAlbumFolder and not os.path.exists(saveFolder):
        print 'Save location "%s" does not exist.' % saveFolder
        sys.exit(2)

    if albumUrl != '':
        albumUrls = [albumUrl]
    elif os.path.exists(urlFilePath):
        for line in open(urlFilePath).readlines():
            albumUrls.append(line.strip())

    for url in albumUrls:
        print '-' * 50
        print 'Preparing to download "%s"' % url
        album = getAlbum(url)
        downloadAlbum(album, saveFolder, createAlbumFolder)

    print 'Done.'

if __name__ == '__main__':
    main(sys.argv[1:])