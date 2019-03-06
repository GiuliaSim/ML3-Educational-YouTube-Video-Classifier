import sys
sys.path.append("..") 
from features.get_background_ratio import get_background_lightning_ratio
import cv2
import os
import csv
import time


INPUT_FILE = "..\\data\\dataset.csv"
OUTPUT_FILE = "..\\data\\aesthetics\\dataset_aesthetic_br.csv"
frames_dir = "..\\frames\\{}\\"
frame_name = "{}{}.bmp"

def format_time(start,end):
	hours, rem = divmod(end-start, 3600)
	minutes, seconds = divmod(rem, 60)
	execut_time = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
	return execut_time
	

if __name__ == '__main__':
	with open(INPUT_FILE, encoding="utf8") as input, open(OUTPUT_FILE, 'w+', newline='') as output:
		writer = csv.writer(output)
		writer.writerow(['videoId','background_lightning_ratio'])
		start = time.time()
		print(f'Start at {time.strftime("%H:%M")}')

		for row in csv.reader(input):
			if row[0] != 'videoId':
				videoId = row[0].replace('/watch?v=','')
				br = get_background_lightning_ratio(videoId)
				print(f'[{videoId}] Background Lightning Ratio: ',br)
				writer.writerow([videoId,br])

		end = time.time()
		print(f'End at {time.strftime("%H:%M")}')
		print('Done in', format_time(start, end))
				
