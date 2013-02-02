tweets-to-files
===============

Take geotagged tweets from the Twitter API and store them in JSON files. By default, they're in ten-minute chunks, and named for their count from the epoch. This script is suitable to leave running on an always-on box.

It is not compatible with forthcoming API changes, but it should be a useful base.

Uses tweetstream for the Twitter API. 

It's commented out in this posted version, but it can also use  http://code.google.com/p/chromium-compact-language-detector/ to guess what langauge tweets are in. (Lately I've preferred to do that on my home machine.)

Search for "SET ME", set those variables, and you should be ready to go.

Not fancy.

To do:
+ update for API changes
+ consider compressing the files from within this script