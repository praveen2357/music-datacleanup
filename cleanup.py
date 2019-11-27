#!/Users/praveenkumaryalal/music-env/bin/python


"""
Idea: create database for music 
track, singers, composers, lyrics writers, year, genre, movie/album
additional:
youtube link
"""
import os
import re
import json

from mutagen.easyid3 import EasyID3

DIR_PATH = os.path.dirname(os.path.abspath(__file__))


special_chars = ['kbps', 'vbr', '320', '190', '128', 'hq']

DIR_PATH = '/Volumes/Untitled/MUSIC/'
data = {}


def clean_dir_names(dir_name):
	dir_name_l = dir_name.lower()
	# replace specical characters with space
	dir_name_l = dir_name_l.replace("-", " ").replace("~", " ").replace("_"," ")
	dir_name_l = dir_name_l.replace("kbps", " ")
	# remove text between parenthesis
	dir_name_l = re.sub(r'\(.*\)',"", dir_name_l)
	dir_name_l = re.sub(r'\[.*\]',"", dir_name_l)
	return dir_name_l


def get_song_info(fpath):
	"""
	sample output:
	{'album': ['Jhoom Barabar Jhoom'], 'composer': ['(SongsMp3.Com)'], 
	'title': ['JBJ (SongsMp3.Com)'], 'version': ['Www.SongsMp3.Com'], 
	'artist': ['SongsMP3.Com, '], 'organization': ['SongsMp3.Com'], 
	'genre': ['Bollywood Songs'], 'date': ['2014']}
	"""
	info = None
	try:
		info = EasyID3(fpath)
	except:
		pass
	return info


def clean_meta_info(path):
	output = []
	for root, dirs, files in os.walk(path):
		for fname in files:
			dir_name = os.path.basename(root)
			fpath = os.path.join(root, fname)
			audio = get_song_info(fpath)
			if (audio is None) or ('date' not in audio):
				continue
			# process the info
			year = audio["date"][0]
			year = year.split('-')[0]
			# get artist
			singers_f = []
			if 'artist' in audio:
				singers = audio["artist"][0]
				singers = list(filter(None, re.split("[,\-&|]+", singers)))
				singers = [v.strip() for v in singers]
				singers = list(set(singers))  # remove duplicates
				for i in range(len(singers)):
					v = singers[i]
					v_l = v.lower()
					if '.com' in v_l or '.me' in v_l or 'www.' in v_l or '.cc' in v_l or '.se' in v_l:
						continue
					elif len(v) == 0:
						continue
					singers_f.append(v)
			# composer
			print(audio)
			composer = ''
			if 'composer' in audio:
				composer = audio["composer"][0]
			# artists
			albumartist = ''
			if 'albumartist' in audio:
				albumartist = audio["albumartist"][0]
			# title 
			title = ''
			if 'title' in audio:
				title = audio["title"][0]
			# genre
			genre = ''
			if 'genre' in audio:
				genre = audio["genre"][0]
			# get album
			album = ''
			if 'album' in audio:
				album = audio["album"][0]
				album = re.sub(r'\(.*\)',"", album)
				album = album.split('-')[0].strip()
			# add to output
			output.append({
				"year": year,
				"singers": ";".join(singers_f),
				"album": album,
				"title": title,
				"composer": composer,
				"genre": genre,
				"albumartist": albumartist,
				"directory": dir_name,
				"file_name": fname,
				"path": fpath
			})
	with open('info.json', 'w') as f:
		f.write(json.dumps(output, indent=4, sort_keys=True))
	


def main(input_args):
	clean_meta_info(DIR_PATH)


if __name__ == "__main__":
	import sys
	input_args = sys.argv[1:]
	main(input_args)
