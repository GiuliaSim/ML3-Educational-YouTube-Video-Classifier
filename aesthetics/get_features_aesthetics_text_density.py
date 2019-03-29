import sys
from features.text_density import get_text_density
import cv2
import os
import csv
import time


INPUT_FILE = "..\\data\\dataset.csv"
OUTPUT_FILE = "..\\data\\aesthetics\\dataset_aesthetic_text_density.csv"
frames_dir = "..\\frames\\{}\\"
frame_name = "{}{}.bmp"

def format_time(start,end):
	hours, rem = divmod(end-start, 3600)
	minutes, seconds = divmod(rem, 60)
	execut_time = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
	return execut_time
	

if __name__ == '__main__':
	with open(INPUT_FILE, encoding="utf8") as input, open(OUTPUT_FILE, 'a', newline='') as output:
		writer = csv.writer(output)
		#writer.writerow(['videoId','text_density'])
		start = time.time()
		print(f'Start at {time.strftime("%H:%M")}')

		count = 0
		for row in csv.reader(input):
			if count >= 227 and row[0] != 'videoId':
				videoId = row[0].replace('/watch?v=','')
				t = get_text_density(videoId)
				print(f'[{videoId}] Text density: ',t)
				writer.writerow([videoId,t])
				output.flush()
			count += 1

		end = time.time()
		print(f'End at {time.strftime("%H:%M")}')
		print('Done in', format_time(start, end))
				
