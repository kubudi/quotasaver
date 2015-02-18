import os
import urllib
import gzip
import glob

from oswrapper import OpenSubtitlesWrapper
from oswrapper import File

class OpenSubtitle(object):
  def __init__(self, username, password, useragent):
    self.username = username
    self.password = password
    self.useragent = useragent

  def decompressFile(self, filePath, targetFile):
    f = gzip.open(filePath, 'rb')
    file_content = f.read()
    f.close()
    os.remove(filePath)
    srtFile = open(targetFile, 'w')
    srtFile.write(file_content)
    srtFile.close

  def downloadSubtitleFromLink(self, link, path, filename):
    testfile = urllib.URLopener()
    testfile.retrieve(link, path + filename + '.gz')
    print(filename + ' subtitle downloaded')
    self.decompressFile(path + filename +'.gz', path + filename + ".srt")

  def downloadSubtitle(self, path, files, subLang):
    ops = OpenSubtitlesWrapper()
    token = ops.login(self.username, self.password, self.useragent)

    for filename in files:
      print(filename + ' subtitle downloading') 
      f = File(path + filename)
      data = ops.search_subtitles([{'sublanguageid': subLang, 'moviehash': f.get_hash(), 'moviebytesize': f.size}])
      if data == False:
        return
      link = str(data[0]['SubDownloadLink'])
      self.downloadSubtitleFromLink(link, path, filename)

    value = ops.logout()

  def downloadSubtitles(self, path, subLang):
    dict = {}
    os.chdir(path)
    for file in glob.glob("*"):
      if "HorribleSubs" in file:
        continue
      elif ".srt" in file:
        dict[file[:-4]] = True
      elif file in dict and dict[file] == True:
        continue
      else:
        dict[file] = False


    files = []
    for movie in dict:
      if dict[movie] == False:
        files.append(movie)
        
    self.downloadSubtitle(path, files, subLang)
    print(str(len(files)) + ' subtitle downloaded')

