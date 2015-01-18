from eztv_api import EztvAPI

def get_links():
  test_api = EztvAPI().tv_show('perception')
  seasons = test_api.seasons()
  for season in seasons:
      for episode in seasons[season]:
          # will print the magnet link of all episodes, in all seasons
          print seasons[season][episode]