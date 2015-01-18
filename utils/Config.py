import ConfigParser

config = ConfigParser.ConfigParser()
config.read('resources/config.ini')

def getstring(section, key):
  return config.get(section, key)

def getint(section, key):
  return config.getint(section, key)
