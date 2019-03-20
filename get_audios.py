import cv2
import os
import csv
import collections
import concurrent.futures

INPUT_FILE = "data\\dataset.csv"
url = 'https://www.youtube.com/watch?v={}'
audios_dir = "audios"
name_file_audio = "{}\\{}\\{}_temp.m4a"

def get_audio(videoId):	
	#download del audio
	#os.system(f'youtube-dl -x --extract-audio --audio-format wav {url.format(videoId)} ')
	os.system(f'youtube-dl -x --extract-audio --audio-format wav {url.format(videoId)} -o {name_file_audio.format(audios_dir,videoId,videoId)}')

if __name__ == '__main__':
	with open(INPUT_FILE, encoding="utf8") as input:
		count = 1

		#creazione della folder dove verranno inseriti gli audio
		if not os.path.exists(audios_dir):
				os.makedirs(audios_dir)

		for row in csv.reader(input):
			if count > 200 and row[0] != 'videoId':
				videoId = row[0].replace('/watch?v=','')
				get_audio(videoId)
				print (videoId + ': Audio salvato')
			count += 1
