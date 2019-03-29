import sys
from features.subject_size import get_subject_size
import cv2
import os
import csv
import time

INPUT_FILE = "..\\data\\dataset.csv"
frames_dir = "..\\frames\\{}\\"
frame_name = "{}{}.bmp"
OUTPUT_FILE_BRIGHTNESS = "..\\data\\aesthetics\\dataset_aesthetic_subject_size.csv"

def format_time(start,end):
	hours, rem = divmod(end-start, 3600)
	minutes, seconds = divmod(rem, 60)
	execut_time = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
	return execut_time

def get_features(row):
	if row[0] != 'videoId':
		videoId = row[0].replace('/watch?v=','')
		s = get_subject_size(videoId)
		print(f'[{videoId}] Subject Size: ',s)
		return videoId, s
	return None, None

if __name__ == '__main__':
	with open(INPUT_FILE, encoding="utf8") as input, open(OUTPUT_FILE_BRIGHTNESS, 'w', newline='') as output:
		start = time.time()
		print(f'Start at {time.strftime("%H:%M")}')
		writer = csv.writer(output)
		header = ['videoId','brightness']
		writer.writerow(header)
		
		count = 0
		for row in csv.reader(input):
			if row[0] != 'videoId':
				videoId, result = get_features(row)
				element = [videoId, result]
				writer.writerow(element)
			count += 1

		end = time.time()
		print(f'End at {time.strftime("%H:%M")}')
		print('Done in', format_time(start, end))

