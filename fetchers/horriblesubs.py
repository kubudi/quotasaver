import os
import json
import httplib
from pyquery import PyQuery as pq

#check animes from horriblesubs
def get_links(watchlist):
  conn = httplib.HTTPConnection("www.horriblesubs.info")
  links = []

  for anime in watchlist:
    name = anime["name"]
    (last_season, last_episode) = anime["lastDownloaded"].split("-")

    conn.request("GET", "/lib/search.php?value=" + name)
    data = conn.getresponse().read()
    dom = pq(data)

    episodes = dom(".episode")
    torrents = dom(".episode > .resolutions-block > .resolution-block > #1080p > .ind-link:nth-child(3) > a")

    for i in range(len(episodes)):
      label =  pq(episodes[i]).attr("id")
      episode =  label.split("-")[-1]
      season =  "01"
      if label.split("-")[-2].isdigit():
        season = label.split("-")[-2]
      if label.split("-")[-2].startswith("s") and label.split("-")[-2][1:].isdigit():
        season = label.split("-")[-2][1:]
      
      if season < 10: 
        season = 0 + season
      if episode < 10: 
        episode = 0 + episode

      if season >= last_season and episode > last_episode:
        link = pq(torrents[i]).attr("href")
        links.append((name, season, episode, link))

  return links