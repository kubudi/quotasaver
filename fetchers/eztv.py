import json

from eztv_api import EztvAPI
from eztv_api import TVShowNotFound

#check shows from EZTV.ch
def get_links(watchlist):
  links = []

  for show in watchlist:
    show_name = show["name"]
    (last_season, last_episode) = show["lastDownloaded"].split("-")

    last_season = int(last_season)
    last_episode = int(last_episode)

    try:
      seasons = EztvAPI().tv_show(show_name).seasons()
      for season in seasons:
        for episode in seasons[season]:
          if (season > last_season or (season == last_season and episode > last_episode)):
            season_name = "0" + str(season) if season < 10 else str(season)
            episode_name = "0" + str(episode) if episode < 10 else str(episode)
            magnet = seasons[season][episode]

            links.append((show_name, season_name, episode_name, magnet))
    except TVShowNotFound as e:
      print e
      pass
    except Exception as e: 
      #do nothing since show is found
      pass

  return links