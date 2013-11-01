# -*- coding: utf-8 -*-

import os
import requests
import argparse

import dl

import eyed3

VERSION = '0.0.2'

URL_PATTERN_ALBUM = 'http://play.baidu.com/data/music/box/album'
URL_PATTERN_SONG = 'http://play.baidu.com/data/music/songlink'
URL_PATTERN_SEARCH = 'http://sug.music.baidu.com/info/suggestion'


SEARCH_PARAM = {
	'format': 'json',
	'from': 0,
	'word': '',
	'version': 2,
	'callback': ''
}

ALBUM_GET_PARAM = {
	'albumId': '',
	'type': 'album'
}

SONG_POST_PARAM = {
	'auto': -1,
	'bat': -1,
	'bp':	-1,
	'bwt': -1,
	'dur': -1,
	'flag': -1,
	'hq': 1,
	'pos': -1,
	'prerate': -1,
	'pt': 0,
	'rate': '',
	's2p': -1,
	'songIds': '',
	'type': 'm4a,mp3'
}


HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
}

def get_song_link(song_id_list):
	song_list = []
	for s in song_id_list:
		song_list.append(int(s))

	SONG_POST_PARAM['songIds'] = str(song_list).strip('[]')
	r = requests.post(URL_PATTERN_SONG, params=SONG_POST_PARAM, headers=HEADERS)
	return r.json()

def download_songs(song_link_list, folder):
	for s in song_link_list['data']['songList']:
		if s['linkinfo'].has_key('320'):
			link = s['linkinfo']['320']['songLink']
		else: 
			link = s['linkinfo']['128']['songLink']
		print '--------------------------downloading----------------'
		print link
		filename = s['songName']
		print filename
		info = {
			'title': s['songName'],
			'album': s['albumName'],
			'artist': s['artistName'],
			'track_num': song_link_list['data']['songList'].index(s)
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
		print '------------------------complete--------------------'
		
def get_song_list(album_id):
	ALBUM_GET_PARAM['albumId'] = album_id
	r = requests.get(URL_PATTERN_ALBUM, params=ALBUM_GET_PARAM, headers=HEADERS)
	return r.json()['data']

def search(query):
	print query
	SEARCH_PARAM['word'] = query
	r = requests.get(URL_PATTERN_SEARCH, params=SEARCH_PARAM, headers=HEADERS)
	data = r.json()['data']
	if data.has_key('album'):
		print '-------------------------Album----------------------------'
		for a in data['album']:
			print a[u'albumname'] +'-'+ a[u'artistname']
			print a[u'albumid']
	if data.has_key('song'):
		print '------------------------Song-------------------------------'
		for s in data['song']:
			print s[u'songname'] +'-'+ s[u'artistname']
			print s[u'songid']
	else:
		print '-----------------------None result------------------------'
		print data

def main():
	args = dl.parse_arguments(VERSION)

	if args.album:
		for a in args.album[0]:
			album = get_song_list(a)
			song_list = get_song_link(album['songIdList'])
			folder = dl.make_folder(album['albumName'])
			download_songs(song_list, folder)

	if args.song:
		song_list = get_song_link(args.song)
		folder = dl.make_folder('')
		download_songs(song_list, folder)

	if args.search:
		search(' '.join(args.search))

if __name__ == '__main__':

	main()