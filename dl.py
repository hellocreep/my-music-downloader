import os
import ConfigParser
import eyed3

cf = ConfigParser.ConfigParser()
cf.read('conf.ini')
DEST = cf.get('dir', 'dest')

def make_folder(name):
	folder = os.path.join(os.getcwd(), DEST, name);
	if not os.path.exists(folder):
		os.makedirs(folder)
	return folder