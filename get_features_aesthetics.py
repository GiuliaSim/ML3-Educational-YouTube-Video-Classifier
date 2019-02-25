from features.brightness import get_brightness
from features.subject_size import get_subject_size
from features.text_density import get_text_density
from features.get_entropy import get_entropy
from features.get_background_ratio import get_background_lightning_ratio
from features.get_bg_simplicity import get_simplicity_feature
import cv2
import os
import csv
import time
import collections
import concurrent.futures
from pprint import pprint


INPUT_FILE = "data\\dataset.csv"
frames_dir = "frames\\{}\\"
frame_name = "{}{}.bmp"

def format_time(start,end):
	minutes, seconds = divmod(end - start, 60) 
	execut_time = "{:0>2}:{:05.2f}".format(int(minutes),seconds)
	return execut_time

def get_features(row):
	if row[0] != 'videoId':
		videoId = row[0].replace('/watch?v=','')
		if os.path.exists(frames_dir.format(videoId)):
			print(f'Process {os.getpid()} working record {videoId}')
			time.sleep(1)
			b = get_brightness(videoId)
			s = get_subject_size(videoId)
			t = get_text_density(videoId)
			e = get_entropy(videoId)
			br = get_background_lightning_ratio(videoId)
			bs = get_simplicity_feature(videoId)
			result = {
				'videoId': videoId,
				'brightness': b,
				'subject_size': s,
				'text_density': t,
				'entropy': e,
				'background_lightning_ratio': br,
				'background_color_simplicity': bs
			}
			print(f'Process {os.getpid()} done procesing record {videoId}')
			return result
		return {'videoId': videoId}

if __name__ == '__main__':
	start = time.time()
	with open(INPUT_FILE, encoding="utf8") as input:
		with concurrent.futures.ThreadPoolExecutor() as executor:
			result = executor.map(get_features, csv.reader(input))
	end = time.time()
	print(f'\nTime to complete: {format_time(start, end)}\n')
	pprint(tuple(result))		

# if __name__ == '__main__':
# 	with open(INPUT_FILE, encoding="utf8") as input:
# 		count = 1
# 		for row in csv.reader(input):
# 			if count < 4 and row[0] != 'videoId':
# 				videoId = row[0].replace('/watch?v=','')
# 				print('[{}]'.format(videoId),' Extracting Features')
# 				start = time.time()
# 				b = get_brightness(videoId)
# 				end_b = time.time()
# 				print('Luminosità in', format_time(start, end_b))
# 				start_s = time.time()
# 				s = get_subject_size(videoId)
# 				end_s = time.time()
# 				print('Subject size in', format_time(start_s, end_s))
# 				start_t = time.time()
# 				t = get_text_density(videoId)
# 				end_t = time.time()
# 				print('Text density in', format_time(start_t, end_t))
# 				start_e = time.time()
# 				e = get_entropy(videoId)
# 				end_e = time.time()
# 				print('Entropy in', format_time(start_e, end_e))
# 				start_br = time.time()
# 				br = get_background_lightning_ratio(videoId)
# 				end_br = time.time()
# 				print('Background Lightning Ratio in', format_time(start_br, end_br))
# 				start_bs = time.time()
# 				bs = get_simplicity_feature(videoId)
# 				end = time.time()
# 				print('Background color simplicity in', format_time(start_bs, end))
# 				print('[{}]'.format(videoId),'in', format_time(start, end))
# 				print('Luminosità: ',b)
# 				print('Subject size: ',s)
# 				print('Text density: ',t)
# 				print('Entropy: ',e)
# 				print('Background Lightning Ratio: ',br)
# 				print('Background color simplicity: ',bs)
# 				count += 1
