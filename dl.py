import os
# import requests
# import re, urllib, urllib2

import eyed3

def make_folder(name):
	folder = os.path.join(os.getcwd(), DEST, name);
	if not os.path.exists(folder):
		os.makedirs(folder)
	return folder

