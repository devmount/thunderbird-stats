#!/usr/bin/python3.6
import os, sys, time, json
from configparser import ConfigParser
from datetime import datetime
# pylint: disable=F0401
from tqdm import tqdm

# get config
cfg = ConfigParser()
cfg.read('config.ini')
# root directory of the maildir account directory of thunderbird
maildir = cfg.get('email', 'ThunderbirdProfilePath')
# own email address(es)
address = cfg.get('email', 'EmailAddresses').split(',')

def stats():
	""" read all mail files, collect and export data """
	mailfiles = []
	meta = { 'in': 0, 'out': 0, 'total': 0 }
	mails_per_year = { 'in': {}, 'out': {} }
	mails_per_month = { 'in': {}, 'out': {} }
	mails_per_hour = { 'in': { i:0 for i in range(24) }, 'out': { i:0 for i in range(24) } }
	mails_per_weekday = { 'in': { i:0 for i in range(7) }, 'out': { i:0 for i in range(7) } }
	# get all mail files
	for root,_,files in os.walk(maildir):
		for f in files:
			_,file_extension = os.path.splitext(f)
			if file_extension == '.eml':
				mailfiles.append(os.path.join(root, f))

	# process all mail files to get data
	for f in tqdm(mailfiles, unit='mails', mininterval=0.05):
		mailtype = None
		maildate = None
		for line in open(f, 'r', encoding='latin1'):
			# determine wether an email was sent or received
			if line.startswith('From:') or line.startswith('from:'):
				mailtype = 'out' if any(a in line for a in address) else 'in'
				continue
			# get mail date
			if line.startswith('Date:'):
				startindex = line.index(',')+2 if ',' in line else line.index(' ')+1
				datestring = line[startindex:].strip()
				datestring = datestring[:datestring.rindex("+")+5] if '+' in datestring else datestring
				try:
					maildate = time.strptime(datestring, '%d %b %Y %H:%M:%S %z')
				except ValueError:
					try:
						datestring = datestring[:datestring.rindex(":")+3]
						maildate = time.strptime(datestring, '%d %b %Y %H:%M:%S')
					except ValueError:
						try:
							maildate = time.strptime(datestring, '%d %b %Y %H:%M')
						except ValueError:
							maildate = None
			# if maildate was not found, try alternative approache/formats
			if maildate is None and ' +0000' in line and len(line)>26:
				datestring = line[line.index(' +0000')-20:line.index(' +0000')+6]
				try:
					maildate = time.strptime(datestring, '%d %b %Y %H:%M:%S %z')
				except ValueError:
					datestring = line[8:26]
					try:
						maildate = time.strptime(datestring, '%Y-%m-%d %H:%M:%S')
					except ValueError:
						datestring = line[6:26]
						try:
							maildate = time.strptime(datestring, '%d %b %Y %H:%M:%S')
						except ValueError:
							maildate = None
			# save found data
			if mailtype is not None and maildate is not None:
				# build meta data
				meta[mailtype] += 1
				meta['total'] += 1
				if 'oldest' not in meta:
					meta['oldest'] = maildate
				if 'newest' not in meta:
					meta['newest'] = maildate
				meta['oldest'] = maildate if maildate < meta['oldest'] else meta['oldest']
				meta['newest'] = maildate if maildate >= meta['newest'] else meta['newest']
				# build mails per year and per month
				if maildate.tm_year in mails_per_year[mailtype]:
					mails_per_year[mailtype][maildate.tm_year] += 1
					mails_per_month[mailtype][maildate.tm_year][maildate.tm_mon] += 1
				else:
					mails_per_year[mailtype][maildate.tm_year] = 1
					mails_per_month[mailtype][maildate.tm_year] = { i:0 for i in range(1,13) }
					mails_per_month[mailtype][maildate.tm_year][maildate.tm_mon] = 1
				# build average mails per hour
				mails_per_hour[mailtype][maildate.tm_hour] += 1
				# build average mails per weekday
				mails_per_weekday[mailtype][maildate.tm_wday] += 1
				# stop and jump to next file
				break
		# for debugging purposes:
		# else:
		# 	if mailtype is None or maildate is None:
		# 		fh = open('./src/data/debug.txt', 'a')
		# 		fh.write(open(f, 'r', encoding='latin1').read())
		# 		fh.close

	# export data
	if not os.path.exists('./src/data/'):
		os.makedirs('./src/data/')
	with open('./src/data/mails-per-year.json', 'w') as f:
		json.dump(mails_per_year, f)
	with open('./src/data/mails-per-month.json', 'w') as f:
		json.dump(mails_per_month, f)
	with open('./src/data/mails-per-hour.json', 'w') as f:
		json.dump(mails_per_hour, f)
	with open('./src/data/mails-per-weekday.json', 'w') as f:
		json.dump(mails_per_weekday, f)
	with open('./src/data/meta.json', 'w') as f:
		# build featured and meta data
		meta['days'] = (time.mktime(meta['newest']) - time.mktime(meta['oldest']))/(60*60*24)
		meta['weeks'] = meta['days']/7
		meta['months'] = meta['days']/(365/12)
		meta['years'] = meta['days']/365
		meta['oldest'] = time.strftime("%Y-%m-%dT%H:%M:%S", meta['oldest'])
		meta['newest'] = time.strftime("%Y-%m-%dT%H:%M:%S", meta['newest'])
		meta['tstamp'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
		json.dump(meta, f, default=json_datetime)

	return True


def json_datetime(obj):
	"""JSON serializer for datetime objects"""
	if isinstance(obj, (datetime)):
		return obj.isoformat()
	raise TypeError ("Type %s not serializable" % type(obj))


# output
print('Processing mails...')
if stats():
	print('Finished.')
