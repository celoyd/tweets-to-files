#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tweetstream, cld

from email.utils import parsedate_tz, mktime_tz # ugh
from datetime import datetime
# from re import sub # turn back on for help with langauge detection
from time import sleep, mktime, gmtime
from json import loads, dumps
from os import rename

from xml.sax.saxutils import unescape

locations = ["-180,-90", "180,90"] # SET ME
uname = '' # SET ME
passwd = '' # SET ME

count = 0
skipped = 0
backoff_power = 2

directory = '' # output directory -- SET ME

def mkfname(h):
	return '%s/%s' % (directory, h)

def clean(s):
	#return s
	return unescape(s)

def epoch():
	return int(mktime(gmtime()))

def timechunk():
	# Not useful for absolute timekeeping, but simple and repeatable.
	return epoch()/60/10

def write_tweet(tweet, ofile):
	global skipped, count, backoff_power
	if not 'coordinates' in tweet or tweet['coordinates'] == None:
		skipped += 1
		return
	
	out = {}
	
	out['tid'] = tweet['id']
	out['uid'] = tweet['user']['id']
	
	date = parsedate_tz(tweet['created_at'])
	date = datetime.fromtimestamp(mktime_tz(date)).strftime('%s')
	out['epoch'] = int(date)
	
	out['screen_name'] = tweet['user']['screen_name']
	out['entities'] = tweet['entities']
	
	out['lon'], out['lat'] = tweet['coordinates']['coordinates']
	
	ulang = tweet['user']['lang']
	
	# Remove usernames:
	#text = sub(r'(@[a-z0-9_]* ?)', r'', tweet['text'])
	# And links:
	#text = sub(r'( https?://[^ ]*)', r'', text)
	# Hashtags stay because they're often in the surrounding language.
	
	#text = text.encode('utf-8')
	
	'''
	if ulang in cld.LANGUAGES:
		detected = cld.detect(text, hintLanguageCode=ulang)
	else:
		detected = cld.detect(text)
	tlang = detected[1]
	
	if tlang == 'un':
		tlangp = None
	else:
		# Estimated probability of the matched language, % => n/1.
		#print detected
		tlangp = detected[4][0][2]/100.0
	'''
	
	out['ulang'] = ulang
	#out['tlang'] = tlang
	#out['tlangp'] = tlangp
	out['inreplyto'] = tweet['in_reply_to_status_id']
	
	out['tweet'] = clean(tweet['text'])
	
	try:
		ofile.write(dumps(out) + '\n')
		#print dumps(out)
	except:
		print 'failed to dumps: ', tweet

if __name__ == '__main__':
	current = timechunk()
	fname = mkfname(current)
	outf = open(fname, 'w')
	
	
	while True:
		try:
			with tweetstream.FilterStream(uname, passwd, locations=locations) as stream:
				for tweet in stream:
					if timechunk() != current:
						current = timechunk()
						new_fname = mkfname(current)
						outf.close()
						try:
							rename(fname, fname + '.done')
						except:
							pass
						fname = new_fname
						outf = open(fname, 'w')
						print 'opening ', fname
					write_tweet(tweet, outf)
		except tweetstream.ConnectionError:
			delay = 2**backoff_power
			print "ConnectionError! Backing off for %s seconds." % (delay)
			sleep(delay)
			if backoff_power < 10:
				backoff_power += 1
