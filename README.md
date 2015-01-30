
quotasaver
===========

What
-----
A python script for checking new episodes of shows/animes and downloading them automatically

Why
----
Becuse it's hard to track all that shows and if you have multiple wathers under same house,
you will certainly have trouble fitting in your quota.(thanks my dear ISP...)

How
---
Last downloaded episode info are being stored for all shows in a json.

Fetchers collect information from resources as ez.tv or horriblesubs. If they provide an api
uses it. Otherwise, parses the html.

If there is a new episode, finds its torrent link(somehow) and sends it to remote transmission client.

With
-----
* transmissionrpc
* pyquery
* beautifulsoup4
* requests
* pyOpenSSL
* pyasn1
* ndg-httpsclient
* json
* [API-EZTV.it](https://github.com/PaulSec/API-EZTV.it)


What to do
----------
Ordered by priority:

* [x] Update *lastDownloaded* value after adding torrent
* [x] An ez.tv fetcher. Library is already here, we need to modify it for torrents(instead of magnets). ( we didn't :) )
* [ ] A subtitle fetcher for tv shows(opensubtitles.com and altyazi.org should be first)
* [ ] An html page for adding shows to watchlist.(template file is already there we need a simple http server and few ajax requests)
* [ ] A Scheduler for running script occasionally.(just cron might be enough)
* [ ] A checklist for storing who watched which episode. 
* [ ] A logic for determining which episode is wathced by all and shoud be removed. And setting *storeSince* value.
* [ ] A cleaner job removes files according to the *storeSince* value.
* [ ] A server for serving files locally.(maybe a mediaserver as well)
* [ ] MOAR fetchers
