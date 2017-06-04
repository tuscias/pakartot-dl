import os
import sys
import argparse
from slugify import slugify
import libpakartot as libpa


def downloadAlbum(albumId, saveFolder, createAlbumFolder=False, downloadCoverArt=False):
    album = libpa.getAlbumInfo(albumId)
    albumName = slugify(album['album_name'])

    if createAlbumFolder:
        saveFolder = os.path.join(saveFolder, albumName)

    if not os.path.exists(saveFolder):
        os.makedirs(saveFolder)

    if downloadCoverArt:
        coverArtUrl = album['photo_path']
        saveLocation =  os.path.join(saveFolder, albumName + '.jpg')
        libpa.downloadCoverArt(coverArtUrl, saveLocation)

    tracks = libpa.getAlbumTracksInfoEx(albumId)
    for i, track in enumerate(tracks):
        trackUrl = track['filename']
        title = slugify(track['title'])
        fileName = "%s.%s.mp3" % (i+1, title)

        saveLocation = os.path.join(saveFolder, fileName)

        libpa.downloadTrack(trackUrl, saveLocation)
        print 'Downloading "%s"' % fileName
    print
    print 'Saved to "%s"' % saveFolder


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

    if albumUrl is not None:
        albumUrls.append(albumUrl)
    else:
        if not os.path.exists(urlFilePath):
            print 'File "%s" does not exist.' % urlFilePath
            sys.exit(2)

        for line in open(urlFilePath).readlines():
            albumUrls.append(line.strip())

    for url in albumUrls:
        print '-' * 50
        print 'Preparing to download "%s"' % url
        albumId = libpa.getAlbumId(url)
        downloadAlbum(albumId, saveFolder, createAlbumFolder, downloadCoverArt)

    print 'Done.'

if __name__ == '__main__':
    main(sys.argv[1:])
