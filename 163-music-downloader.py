# -*- coding: utf-8 -*-

import os
import requests
import re, urllib, urllib2
import argparse

import dl

import eyed3

VERSION = '0.0.1'

URL_PATTERN_ALBUM = 'http://music.163.com/api/album/'

URL_PATTERN_SEARCH = 'http://music.163.com/api/search/suggest/web?csrf_token='

ALBUM_GET_PARAM = {
	'id': '',
	'csrf_token': ''
}
SONG_POST_PARAM = {
	
}

HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
	'Referer': 'http://music.163.com/'
}

DEST = dl.DEST

def parse_arguments():

	note = 'The following SONG, ALBUM, and PLAYLIST are IDs which can be' \
           'obtained from the URL of corresponding web page.'

	parser = argparse.ArgumentParser(description=note)

	parser.add_argument('-v', '--version', action='version', version=VERSION)
	parser.add_argument('-a', '--album',
                        help='adds all songs in the albums for download',
                        type=int, nargs='+')
	parser.add_argument('-s', '--song',
                        help='add a songs in the albums for download',
                        type=int, nargs='+')
	parser.add_argument('-se', '--search',
                        help='search song',
                        type=str, nargs='+')

	return parser.parse_args()

def set_song_info(filename, info):
	audio = eyed3.load(filename)
	audio.tag.title = info[u'title']
	audio.tag.album = info[u'album']
	audio.tag.artist = info[u'artist']
	audio.tag.track_num = info[u'track_num']
	audio.tag.save()

def download_song(songs, folder, album_cover):
	for s in songs:
		# if s['linkinfo'].has_key('320'):
		# 	link = s['linkinfo']['320']['songLink']
		# else: 
		# 	link = s['linkinfo']['128']['songLink']
		link = s['mp3Url']
		print '--------------------------downloading----------------'
		print link
		filename = s['name']
		print filename
		info = {
			'title': s['name'],
			'album': s['album']['name'],
			'artist': s['artists'][0]['name'],
			'track_num': songs.index(s)
		}
		output_file = os.path.join(folder, filename+'.mp3')
		r = requests.get(link, headers=HEADERS, stream=True)
		r.encoding = 'utf-8'
		with open(output_file, 'wb') as output:
			for chunk in r.iter_content(1024):
				if not chunk:
					break
				output.write(chunk)
		set_song_info(output_file, info)	
		print '------------------------complete--------------------'
		
def get_album(album_id):
	ALBUM_GET_PARAM['id'] = album_id
	r = requests.get(URL_PATTERN_ALBUM+str(album_id), params=ALBUM_GET_PARAM, headers=HEADERS)
	data = r.json()

	if data.has_key('album'):	
		return r.json()['album']
	else:
		print data
		return False

def main():
	args = parse_arguments()

	if args.album:
		for a in args.album:
			data = get_album(a)
			if data:
				folder = dl.make_folder(data['name'])
				download_song(data['songs'], folder, data['picUrl'])
	# TODO
	if args.song:
		for s in args.song:
			song_list = get_song_link(s)
			print song_list
	if args.search:
		search(' '.join(args.search))

def search(query):
	print query
	r = requests.post(URL_PATTERN_SEARCH, params={'limit': 20, 's': query}, headers=HEADERS)

	data = r.json()['result']
	if data.has_key('albums'):
		print '-------------------------Album----------------------------'
		for a in data['albums']:
			print a[u'name'] +'-'+ a['artist'][u'name']
			print a['id']
	if data.has_key('songs'):
		print '------------------------Song-------------------------------'
		for s in data['songs']:
			print s[u'name'] +'-'+ s['artists'][0][u'name']
			print s['id']
	else:
		print '-----------------------None result------------------------'
		print data

if __name__ == '__main__':
	
	main()