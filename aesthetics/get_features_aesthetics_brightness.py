from features.brightness import get_brightness
from features.subject_size import get_subject_size
from features.text_density import get_text_density
import cv2
import os
import csv
import time

INPUT_FILE = "data\\dataset.csv"
frames_dir = "frames\\{}\\"
frame_name = "{}{}.bmp"
OUTPUT_FILE_BRIGHTNESS = "data\\dataset_aesthetic_brightness.csv"

def get_features(row):
	if row[0] != 'videoId':
		videoId = row[0].replace('/watch?v=','')
		b = get_brightness(videoId)
		print('get_brightness: ',videoId,b)
		return videoId, b
	return None, None



if __name__ == '__main__':
	start = time.time()
	with open(INPUT_FILE, encoding="utf8") as input, open(OUTPUT_FILE_BRIGHTNESS, 'w', newline='') as output:
		writer = csv.writer(output, delimiter="\t")
		header = ['videoId','brightness']
		writer.writerow(header)
		for row in csv.reader(input):
			videoId, result = get_features(row)
			element = [videoId, result]
			writer.writerow(element)

			


