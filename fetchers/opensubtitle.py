import os
from urllib import URLopener
import gzip
import glob

from oswrapper import OpenSubtitlesWrapper
from oswrapper import File


class OpenSubtitle(object):

    def __init__(self, username, password, useragent):
        self.username = username
        self.password = password
        self.useragent = useragent

    def decompress_file(self, filePath, targetFile):
        f = gzip.open(filePath, 'rb')
        file_content = f.read()
        f.close()
        os.remove(filePath)
        srtFile = open(targetFile, 'w')
        srtFile.write(file_content)
        srtFile.close

    def download_from_link(self, link, path, filename):
        URLopener().retrieve(link, path + filename + '.gz')
        print(filename + ' subtitle downloaded')
        self.decompress_file(path + filename + '.gz', path + filename + ".srt")

    def download(self, path, files, subLang):
        ops = OpenSubtitlesWrapper()
        ops.login(self.username, self.password, self.useragent)

        for filename in files:
            print(filename + ' subtitle downloading')
            f = File(path + filename)
            data = ops.search_subtitles([{'sublanguageid': subLang,
                                          'moviehash': f.get_hash(),
                                          'moviebytesize': f.size}])
            if not data:
                return
            link = str(data[0]['SubDownloadLink'])
            self.download_from_link(link, path, filename)

        ops.logout()

    def download_subs(self, path, subLang):
        dict = {}
        os.chdir(path)
        for file in glob.glob("*"):
            if "HorribleSubs" in file:
                continue
            elif ".srt" in file:
                dict[file[:-4]] = True
            elif file in dict and dict[file]:
                continue
            else:
                dict[file] = False

        files = []
        for movie in dict:
            if not dict[movie]:
                files.append(movie)

        self.download(path, files, subLang)
        print(str(len(files)) + ' subtitle downloaded')
