# -*- coding: utf-8 -*-

import os
import ConfigParser
import argparse
import eyed3

def get_dest():
	cf = ConfigParser.ConfigParser()
	cf.read('conf.ini')
	DEST = cf.get('dir', 'dest')
	return DEST

def make_folder(name):
	DEST = get_dest()

	folder = os.path.join(os.getcwd(), DEST, name);
	if not os.path.exists(folder):
		os.makedirs(folder)
	return folder

def parse_arguments(VERSION):

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
                        help='search album or song',
                        type=str, nargs='+')

	return parser.parse_args()

def set_song_info(filename, info):
	audio = eyed3.load(filename)
	audio.tag.title = info[u'title']
	audio.tag.album = info[u'album']
	audio.tag.artist = info[u'artist']
	audio.tag.track_num = info[u'track_num']
	audio.tag.save()