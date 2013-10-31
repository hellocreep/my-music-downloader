# -*- coding: utf-8 -*-

import os
import requests
import re, urllib, urllib2
import argparse

import dl

import eyed3

VERSION = '0.0.1'

URL_PATTERN_ALBUM = 'http://play.baidu.com/data/music/box/album'
URL_PATTERN_SONG = 'http://play.baidu.com/data/music/songlink'

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


f = open('conf.ini', 'r')
DEST = f.read().strip().split('=')[1].replace('\\','\\\\')
f.close()

def parse_arguments():

	note = 'The following SONG, ALBUM, and PLAYLIST are IDs which can be' \
           'obtained from the URL of corresponding web page.'

	parser = argparse.ArgumentParser(description=note)

	parser.add_argument('-v', '--version', action='version', version=VERSION)
	parser.add_argument('-a', '--album', action='append',
                        help='adds all songs in the albums for download',
                        type=int, nargs='+')
	parser.add_argument('-s', '--song', action='append',
                        help='add a songs in the albums for download',
                        type=int, nargs='+')

	return parser.parse_args()

def set_song_info(filename, info):
	print info['title']
	audio = eyed3.load(filename)
	audio.tag.title = info[u'title']
	audio.tag.album = info[u'album']
	audio.tag.artist = info[u'artist']
	audio.tag.track_num = info[u'track_num']
	audio.tag.save()

def get_song_link(song_id_list):
	song_list = []
	for s in song_id_list:
		song_list.append(int(s))

	SONG_POST_PARAM['songIds'] = str(song_list).strip('[]')
	r = requests.post(URL_PATTERN_SONG, params=SONG_POST_PARAM, headers=HEADERS)
	return r.json()

def download_song(song_link_list, folder):
	for s in song_link_list['data']['songList']:
		if s['linkinfo'].has_key('320'):
			link = s['linkinfo']['320']['songLink']
		else: 
			link = s['linkinfo']['128']['songLink']
		print '--------------------------downloading----------------'
		print link
		filename = s['songName']
		info = {
			'title': s['songName'],
			'album': s['albumName'],
			'artist': s['artistName'],
			'track_num': song_link_list['data']['songList'].index(s)
		}
		output_file = os.path.join(folder, filename+'.mp3')
		# request = urllib2.Request(link)
		# request.add_header('User-Agent', HEADERS['User-Agent'])
		# response = urllib2.urlopen(request)
		r = requests.get(link, headers=HEADERS, stream=True)
		r.encoding = 'utf-8'
		with open(output_file, 'wb') as output:
			for chunk in r.iter_content(1024):
				if not chunk:
					break
				output.write(chunk)
		set_song_info(output_file, info)
		print '------------------------complete--------------------'
		
def get_song_list(album_id):
	ALBUM_GET_PARAM['albumId'] = album_id
	r = requests.get(URL_PATTERN_ALBUM, params=ALBUM_GET_PARAM, headers=HEADERS)
	dl.make_folder(r.json()['data']['albumName'])
	return r.json()['data']

# def make_folder(name):
# 	folder = os.path.join(os.getcwd(), DEST, name);
# 	if not os.path.exists(folder):
# 		os.makedirs(folder)
# 	return folder

def search(query):
	return None

def main():
	args = parse_arguments()

	if args.album:
		for a in args.album[0]:
			data = get_song_list(a)
			song_list = get_song_link(data['songIdList'])
			folder = dl.make_folder(data['albumName'])
			download_song(song_list, folder)
	if args.song:
		for s in args.song:
			song_list = get_song_link(s)
			download_song(song_list, DEST)

if __name__ == '__main__':

	main()