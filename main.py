import transmissionrpc
import os
import json
import httplib

from utils import Config as conf
from fetchers.opensubtitle import OpenSubtitle
from fetchers import horriblesubs
from fetchers import eztv

def update_last_download(download_list, watchlist, file_name):
  last_down = {}
  for (name, season, episode, link) in download_list:
    if name not in last_down.keys():
      last_down[name] = {"season": season, "episode": episode}
    else:
      if last_down[name]["season"] < season:
        last_down[name]["season"] = season
      if last_down[name]["episode"] < episode:
        last_down[name]["episode"] = episode


  for item in watchlist:
    name = item["name"]
    if name in last_down.keys():
      item["lastDownloaded"] = last_down[name]["season"] + "-" + last_down[name]["episode"]

  json.dump(watchlist, open(file_name, 'w'), indent=4, sort_keys=True)

#get the client
host = conf.getstring("Transmission", "host")
port = conf.getint("Transmission", "port")
client = transmissionrpc.Client(host, port=port)

links = []
magnets = []

#horriblesubs
anime_file = 'resources/anime_watchlist'
anime_watchlist = json.load(open(anime_file, 'r'))
anime_links = horriblesubs.get_links(anime_watchlist)
links += anime_links
 
#eztv.ch
show_file = 'resources/show_watchlist'
show_watchlist = json.load(open(show_file, 'r'))
show_magnets = eztv.get_links(show_watchlist)
magnets += show_magnets

#add other fetchers here
###

#fetch torrent from link
for link in links:
  client.add_torrent(link[3])

#fetch torrent from magnet
for magnet in magnets:
  client.add(None, filename=magnet[3])

#update last downloaded shows info in watch lists
update_last_download(anime_links, anime_watchlist, anime_file)
update_last_download(show_magnets, show_watchlist, show_file)

#OpenSubtitle Configs
username = conf.getstring("OpenSubtitle", "username")
password = conf.getstring("OpenSubtitle", "password")
useragent = conf.getstring("OpenSubtitle", "useragent")
sublang = conf.getstring("OpenSubtitle", "sublang")
sourcepath = conf.getstring("OpenSubtitle", "sourcepath")

# Get Series Subtitles except animes
opensub = OpenSubtitle(username, password, useragent)
opensub.download_subs(sourcepath, sublang)
