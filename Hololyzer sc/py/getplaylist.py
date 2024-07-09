#!/usr/bin/env python
from pytube import YouTube, Playlist
import sys
import urllib.request
import urllib

playlistid = sys.argv[1]

if(playlistid.startswith("list=PL") == False):
	sys.exit(0)

playlist_link = "https://www.youtube.com/playlist?" + playlistid.strip()
video_links = Playlist(playlist_link).video_urls

videostring=""
for v in video_links:
	videostring = videostring + "\n" + v.split("?v=")[1]
videostring = videostring.strip()
print(videostring)
