Hololyzer Data scraper.
(see "how to use" below)

>> ** Requirements ** <<
----------------------
-- bash
-- python3
-- pandas

=== FILE DESCRIPTIONS ===
-------------------
scraper.sh [videoID] [-p]
# example command 1: bash scraper.sh "KuI2jajS4FU"
# example command 2: bash scraper.sh -p
> Either takes a single video ID, or the "-p" flag which tells it to read from a list of ID's.
> HTML files are downloaded if they don't already exist in the folder. 
** If the page doesn't exist on Hololyzer a warning is given.
> automatically runs process.py to compile the html file into usable data
> produces a .csv file for charting, and a full .txt file with detailed information.
~ Video ID ~
It's an 11 digit code found in the URL of any youtube video:
EX] 	https://www.youtube.com/watch?v=fsc91rJUdUE
	the ID for this one is: fsc91rJUdUE
	
list.txt
> is read by scraper.sh with the "-p" flag
Formatted as follows:
	~ Bijou
	KuI2jajS4FU
	https://www.youtube.com/playlist?list=PLpy43bHw-UIW45btN-63dg1kqX4WuQ9Sw
> The title of the data can occupy any line, flagged by "~ " at the beginning. 
> video ID's can be listed manually, or entire playlists as well

Currencies.txt
A list of known currencies under their regions. Can be adjusted at will. 
> If a currency is not known, a warning is given and the region will be labelled "Unknown"
> Regions are flagged by "~ " at the beginning of the line
Formatted as follows:

	~ European
	EUR
	GBP
	SEK
	NOK

	~ Western
	USD
	CAD
	AUD

	~ Asian
	YEN
	TWD
	HKD
> Currency names are the second column on Hololyzer "cur", but if missing, the first column is used "sign"
** a common case of this is "ZAR"
	
	
=== HOW TO USE ===
------------------
Step 1) Overview Currencies.txt and make sure the categories are to your liking. 
Step 2) Select which video ID's you want to include.
Step 3) Run Scraper.sh, check any warnings or errors given.
Step 4) Find the output in the "data" folder
Step 5) Be careful your data isn't overwritten. Move the filex to a different folder and rename


