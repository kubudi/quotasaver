import os
import json
import httplib
from pyquery import PyQuery as pq

#check animes from horriblesubs
def get_links():
  watch_list_file = open('resources/watchlist', 'r')
  watch_list = json.load(watch_list_file)

  conn = httplib.HTTPConnection("www.horriblesubs.info")

  links = []

  for anime in watch_list:
    anime_name = anime["name"]
    (last_downloaded_season, last_downloaded_episode) = anime["lastDownloaded"].split("-")

    conn.request("GET", "/lib/search.php?value=" + anime_name)
    data = conn.getresponse().read()

    dom = pq(data)

    episodes = dom(".episode")
    torrents = dom(".episode > .resolutions-block > .resolution-block > #1080p > .ind-link:nth-child(3) > a")

    for i in range(len(episodes)):
      name =  pq(episodes[i]).attr("id")
      episode =  name.split("-")[-1]
      season =  "00"
      if name.split("-")[-2].isdigit():
        season = name.split("-")[-2]
      if name.split("-")[-2].startswith("s"):
        season = name.split("-")[-2][1:]
      if season > last_downloaded_season and episode > last_downloaded_episode:
        links.append(pq(torrents[i]).attr("href"))

  return links