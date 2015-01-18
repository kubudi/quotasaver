import transmissionrpc
import os
import json
import httplib


from utils import Config as conf
from fetchers import horriblesubs
from fetchers import eztv

#get the client
host = conf.getstring("Transmission", "host")
port = conf.getint("Transmission", "port")
client = transmissionrpc.Client(host, port=port)

#add other fetchers here
links = []
links += horriblesubs.get_links()
#eztv.get_links()

for link in links:
  client.add_torrent(link)