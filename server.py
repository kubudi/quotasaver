from flask import Flask, request, jsonify
from flask import render_template
import json

app = Flask(__name__)

status_success = {"status": "success"}
status_already_exists = {"status": "already exists"}

@app.route('/watchlist')
def hello():
  animelist = json.load(open("resources/anime_watchlist", 'r'))
  showlist = json.load(open("resources/show_watchlist", 'r'))
  shows = []
  animes = []
  for show in animelist:
    animes.append(show["name"].lower())

  for show in showlist:
    shows.append(show["name"].lower())

  return render_template('watchlist.html', shows=shows, animes=animes)


@app.route('/watchlist/add', methods=['POST'])
def newShow():
  data = request.json

  typ = data["type"]
  del data['type']

  data["name"] = data["name"].lower()

  res = ""
  if typ == "show":
    res = add_show(data)
  elif typ == "anime":
    res = add_anime(data)

  print res
  return jsonify(res)

def add_show(data):
  return add(data, 'resources/show_watchlist')

def add_anime(data):
  return add(data, 'resources/anime_watchlist')

def add(data, file_name):
  fd = open(file_name, 'r+')
  watchlist = json.load(fd)
  name = data["name"]

  exists = False

  for show in watchlist:
    if show["name"].lower() == name:
      exists = True
      break

  if not exists:
    watchlist.append(data)
    fd.seek(0)
    json.dump(watchlist, fd, indent=4, sort_keys=True)
    fd.truncate()
    fd.close
    return status_success
  else:
    return status_already_exists

if __name__ == "__main__":
  app.debug = True
  app.run()
  # app.run(host='0.0.0.0')