# pakartot-dl
Install dependencies:
```
pip install python-slugify
```

Run the script:
```
python pakartot-dl.py -u https://www.pakartot.lt/album/vaiku-kambarys -s D:\dainos\ -c
```

Parameters:
```
-u    Scrape album data from url and download all files
-s    Folder location where all downloaded files should be saved
-f    Batch mode: download multiple albums by specifying urls in a file (one url in a line)    
-c    Create an album folder in the <saveFolderLocation> and download  all file there
```
