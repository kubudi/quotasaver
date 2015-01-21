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

links = []

#add other fetchers here
anime_watchlist = json.load(open('resources/anime_watchlist', 'r'))
anime_links = horriblesubs.get_links(anime_watchlist)
#links += eztv.get_links()

links += anime_links

for link in links:
  client.add_torrent(link[3])


#update last downloaded
last_down = {}
for (name, season, episode, link) in anime_links:
  if name not in last_down.keys():
    last_down[name] = {"season": season, "episode": episode}
  else:
    if last_down[name]["season"] < season:
      last_down[name]["season"] = season
    if last_down[name]["episode"] < episode:
      last_down[name]["episode"] = episode


for anime in anime_watchlist:
  name = anime["name"]
  if name in last_down.keys():
    anime["lastDownloaded"] = last_down[name]["season"] + "-" + last_down[name]["episode"]

json.dump(anime_watchlist, open('resources/anime_watchlist', 'w'), indent=4, sort_keys=True)