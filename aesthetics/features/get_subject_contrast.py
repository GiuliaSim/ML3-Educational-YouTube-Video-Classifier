import numpy as np
import os
import math
import statistics
import cv2 as cv2

frames_dir = "..\\..\\frames\\{}\\"
file_name="temp.mp4"
frameSg_name="temp-fram.jpg"

def get_subject_contrast(videoId):
    b = []
    if os.path.exists(frames_dir.format(videoId)):
	    for file in os.listdir(frames_dir.format(videoId)):
	        if file.endswith(".bmp"):
	            image_path = os.path.join(frames_dir.format(videoId), file)
	            #print (image_path)
	            #img = cv2.imread(image_path)
	            #img = cv2.cvtColor(image_path, cv2.COLOR_BGR2GRAY)
	            iesimo = subtract_background(image_path, videoId)
	            if (iesimo is not None):
	            	b.append(iesimo)            
    #print ("totale :")
    mean = (statistics.mean(b) if b else 'None')
    return mean

def subtract_background(image_path, videoId):
	fgbg = cv2.createBackgroundSubtractorMOG2()
	frame = cv2.imread(image_path)
	fgmask = fgbg.apply(frame)
	cv2.imwrite((frames_dir.format(videoId) + frameSg_name), fgmask)
	frameSg = cv2.imread(frames_dir.format(videoId) + frameSg_name)
	luminositaFrame = calcoloBightness(frame)
	luminotsitaSogetto = calcoloBightness(frameSg)
	luminositaBack = (luminositaFrame - luminotsitaSogetto)

	if(luminositaBack != 0):
		a = math.pow((luminotsitaSogetto / luminositaBack),2)
		a = math.sqrt(a)
		b = np.log2(a)
		#print(b)
	return b
       	
def calcoloBightness(image):
	image_hsv = cv2.cvtColor(image,cv2.COLOR_RGB2HSV)
	h, s, v = cv2.split(image_hsv)
	brightness = v.mean()
	return brightness
