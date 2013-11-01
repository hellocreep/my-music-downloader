# -*- coding: utf-8 -*-

import os
import requests
import argparse

import dl

VERSION = '0.0.2'

URL_PATTERN_ALBUM = 'http://music.163.com/api/album/'

URL_PATTERN_SONG = 'http://music.163.com/api/song/detail/'

URL_PATTERN_SEARCH = 'http://music.163.com/api/search/suggest/web?csrf_token='

ALBUM_GET_PARAM = {
	'id': '',
	'csrf_token': ''
}

SONG_GET_PARAM = {
	'csrf_token': '',
	'id': '',
	'ids': ''
}

HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
	'Referer': 'http://music.163.com/'
}

def download_songs(songs, folder):
	for s in songs:
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
		dl.set_song_info(output_file, info)	
		print '--------------------------complete--------------------'

def get_songs(songids): 
	SONG_GET_PARAM['ids'] = str(songids)
	r = requests.get(URL_PATTERN_SONG, params=SONG_GET_PARAM, headers=HEADERS)
	if r.json().has_key('songs') and len(r.json()['songs']) > 0:
		return r.json()['songs']
	else:
		return False
		
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
	args = dl.parse_arguments(VERSION)

	if args.album:
		for a in args.album:
			album = get_album(a)
			if album:
				folder = dl.make_folder(album['name'])
				download_songs(album['songs'], folder)
	if args.song:
		songs = get_songs(args.song)
		if songs:
			folder = dl.make_folder('')
			download_songs(songs, folder)

	if args.search:
		search(' '.join(args.search))
# TODO
# QUERY 中文参数问题
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