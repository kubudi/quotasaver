import os
import struct

from xmlrpclib import ServerProxy

class OpenSubtitlesWrapper(object):
    '''OpenSubtitles API wrapper.

    Please check the official API documentation at:
    http://trac.opensubtitles.org/projects/opensubtitles/wiki/XMLRPC
    '''

    def __init__(self):
        self.xmlrpc = ServerProxy('http://api.opensubtitles.org/xml-rpc', allow_none=True)
        self.language = 'en'
        self.token = None

    def _get_from_data_or_none(self, key):
        '''Return the key getted from data if the status is 200,
        otherwise return None.
        '''
        status = self.data.get('status').split()[0]
        return self.data.get(key) if '200' == status else None

    def login(self, username, password, useragent):
        '''Returns token is login is ok, otherwise None.
        '''
        self.data = self.xmlrpc.LogIn(username, password,
                                 self.language, useragent)
        token = self._get_from_data_or_none('token')
        if token:
            self.token = token
        return token

    def logout(self):
        '''Returns True is logout is ok, otherwise None.
        '''
        data = self.xmlrpc.LogOut(self.token)
        return '200' in data.get('status')

    def search_subtitles(self, params):
        '''Returns a list with the subtitles info.
        '''
        self.data = self.xmlrpc.SearchSubtitles(self.token, params)
        return self._get_from_data_or_none('data')

    def no_operation(self):
        '''Return True if the session is actived, False othercase.

        .. note:: this method should be called 15 minutes after last request to
                  the xmlrpc server.
        '''
        data = self.xmlrpc.NoOperation(self.token)
        return '200' in data.get('status')

    def auto_update(self, program):
        '''Returns info of the program: last_version, url, comments...
        '''
        data = self.xmlrpc.AutoUpdate(program)
        return data if '200' in data.get('status') else None

    def search_movies_on_imdb(self, params):
        self.data = self.xmlrpc.SearchMoviesOnIMDB(self.token, params)
        return self.data

class File(object):
    def __init__(self, path):
        self.path = path
        self.size = os.path.getsize(path)

    def get_hash(self):
        '''Original from: http://goo.gl/qqfM0
        '''
        longlongformat = 'q'  # long long
        bytesize = struct.calcsize(longlongformat)

        try:
            f = open(self.path, "rb")
        except(IOError):
            return "IOError"

        hash = int(self.size)

        if int(self.size) < 65536 * 2:
            return "SizeError"

        for x in range(65536 / bytesize):
            buffer = f.read(bytesize)
            (l_value, ) = struct.unpack(longlongformat, buffer)
            hash += l_value
            hash = hash & 0xFFFFFFFFFFFFFFFF  # to remain as 64bit number

        f.seek(max(0, int(self.size) - 65536), 0)
        for x in range(65536 / bytesize):
            buffer = f.read(bytesize)
            (l_value, ) = struct.unpack(longlongformat, buffer)
            hash += l_value
            hash = hash & 0xFFFFFFFFFFFFFFFF

        f.close()
        returnedhash = "%016x" % hash
        return str(returnedhash)