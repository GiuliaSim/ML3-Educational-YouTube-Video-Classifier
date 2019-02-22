from features.brightness import get_brightness
from features.subject_size import get_subject_size
from features.text_density import get_text_density
import cv2
import os
import csv

INPUT_FILE = "data\\dataset.csv"
frames_dir = "frames\\{}\\"
frame_name = "{}{}.bmp"


if __name__ == '__main__':
	with open(INPUT_FILE, encoding="utf8") as input:
		count = 1
		for row in csv.reader(input):
			if count < 4 and row[0] != 'videoId':
				videoId = row[0].replace('/watch?v=','')
				b = get_brightness(videoId)
				s = get_subject_size(videoId)
				t = get_text_density(videoId)
				print('Luminosità: ',videoId,b)
				print('Subject size: ',videoId,s)
				print('Text density: ',videoId,t)
				count += 1
