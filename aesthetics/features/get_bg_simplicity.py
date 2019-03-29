import numpy as np
import os
import datetime
import math
import statistics
import cv2 as cv2

frames_dir = "..\\..\\frames\\{}\\"

def get_simplicity_feature(videoId):
	b = []
	#print(datetime.datetime.now())
	if os.path.exists(frames_dir.format(videoId)):
		for file in os.listdir(frames_dir.format(videoId)):
			if file.endswith(".bmp"):
				image_path = os.path.join(frames_dir.format(videoId), file)
				b.append(simplicity_frame(image_path))
	#print(datetime.datetime.now())
	
	mean = (statistics.mean(b) if b else 'None')
	return mean

def simplicity_frame(frame_path):
	frame = cv2.imread(frame_path, 1)
	totalBins = 4096
	hist = [0]*totalBins
	gamma = 0.01
	total = 0
	for col in frame:
		for pixel in col:
			bin = (pixel[2] / 16) * (pixel[1] / 16) * pixel[0] / 16
			pos = int(bin)
			hist[pos]+=1
	hmax = np.amax(hist)
	s = 0
	den = gamma * hmax
	for i in hist:
		if i >= den:
			s = s + 1
	
	return s / totalBins
