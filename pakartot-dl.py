import os
import sys
import json
import urllib
import urllib2
import argparse
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

def downloadAlbum(album, saveFolder, createAlbumFolder=False, downloadCoverArt=False):
    response = doRequest('play', {'action': 'album', 'id': album['album_id']})
    data = json.loads(response.read())

    if createAlbumFolder:
        saveFolder = os.path.join(saveFolder, slugify(album['album_name']))

    if not os.path.exists(saveFolder):
        os.makedirs(saveFolder)

    if downloadCoverArt:
        coverArtUrl = album['photo_path']
        coverArtContent = urllib2.urlopen(coverArtUrl).read()
        coverSaveLocation = os.path.join(saveFolder, 'cover.jpg')

        with open(coverSaveLocation, 'wb') as f:
            f.write(coverArtContent)

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
    parser = argparse.ArgumentParser(description='Downloads mp3 from pakartot.lt site')
    parser.add_argument('-u', '--url', help='An url. If not given, -f is required')
    parser.add_argument('-f', '--file', help='A text file with urls separated by new lines. If not given, -u is required')
    parser.add_argument('-s', '--save-folder', type=str, required=True, help='A folder (required)')
    parser.add_argument('-c', action='store_true', help='Create separate album folder')
    parser.add_argument('-a', action='store_true', help='Download album cover-art')

    args = parser.parse_args(argv)
    if not args.url and not args.file:
        parser.error ('either -u or -f is required.')

    albumUrls = []
    albumUrl = args.url
    urlFilePath = args.file
    saveFolder = args.save_folder
    createAlbumFolder = args.c
    downloadCoverArt = args.a

    if not createAlbumFolder and not os.path.exists(saveFolder):
        print 'Save location "%s" does not exist.' % saveFolder
        sys.exit(2)

    if albumUrl != '':
        albumUrls.append(albumUrl)
    elif os.path.exists(urlFilePath):
        for line in open(urlFilePath).readlines():
            albumUrls.append(line.strip())

    for url in albumUrls:
        print '-' * 50
        print 'Preparing to download "%s"' % url
        album = getAlbum(url)
        downloadAlbum(album, saveFolder, createAlbumFolder, downloadCoverArt)

    print 'Done.'

if __name__ == '__main__':
    main(sys.argv[1:])
