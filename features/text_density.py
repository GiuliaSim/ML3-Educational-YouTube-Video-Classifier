# import the necessary packages
from imutils.object_detection import non_max_suppression
import numpy as np
import argparse
import time
import cv2
import os
import statistics

frames_dir = "..\\frames\\{}\\"
EAST_PATH = "..\\frozen_east_text_detection.pb"

def get_text_density_frame(image_path):
	image = cv2.imread(image_path)

	# large = cv2.imread(image_path)
	# rgb = cv2.pyrDown(large)
	# small = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

	# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
	# grad = cv2.morphologyEx(small, cv2.MORPH_GRADIENT, kernel)

	# _, bw = cv2.threshold(grad, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

	# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
	# connected = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)
	# # using RETR_EXTERNAL instead of RETR_CCOMP
	# contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	# #For opencv 3+ comment the previous line and uncomment the following line
	# #_, contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	# mask = np.zeros(bw.shape, dtype=np.uint8)

	# for idx in range(len(contours)):
	#     x, y, w, h = cv2.boundingRect(contours[idx])
	#     mask[y:y+h, x:x+w] = 0
	#     cv2.drawContours(mask, contours, idx, (255, 255, 255), -1)
	#     r = float(cv2.countNonZero(mask[y:y+h, x:x+w])) / (w * h)

	#     if r > 0.45 and w > 8 and h > 8:
	#         cv2.rectangle(rgb, (x, y), (x+w-1, y+h-1), (0, 255, 0), 2)

	# cv2.imshow('rects', rgb)
	# cv2.waitKey(0)

	orig = image.copy()
	(H, W) = image.shape[:2]
	 
	# set the new width and height and then determine the ratio in change
	# for both the width and height
	(newW, newH) = (320, 320)
	rW = W / float(newW)
	rH = H / float(newH)
	 
	# resize the image and grab the new image dimensions
	image = cv2.resize(image, (newW, newH))
	(H, W) = image.shape[:2]

	# define the two output layer names for the EAST detector model that
	# we are interested -- the first is the output probabilities and the
	# second can be used to derive the bounding box coordinates of text
	layerNames = [
		"feature_fusion/Conv_7/Sigmoid",
		"feature_fusion/concat_3"]

	# load the pre-trained EAST text detector
	#print("[INFO] loading EAST text detector...")
	net = cv2.dnn.readNet(EAST_PATH)
	 
	# construct a blob from the image and then perform a forward pass of
	# the model to obtain the two output layer sets
	blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
		(123.68, 116.78, 103.94), swapRB=True, crop=False)
	start = time.time()
	net.setInput(blob)
	(scores, geometry) = net.forward(layerNames)
	end = time.time()
	 
	# show timing information on text prediction
	#print("[INFO] text detection took {:.6f} seconds".format(end - start))

	# grab the number of rows and columns from the scores volume, then
	# initialize our set of bounding box rectangles and corresponding
	# confidence scores
	(numRows, numCols) = scores.shape[2:4]
	rects = []
	confidences = []
	 
	# loop over the number of rows
	for y in range(0, numRows):
		# extract the scores (probabilities), followed by the geometrical
		# data used to derive potential bounding box coordinates that
		# surround text
		scoresData = scores[0, 0, y]
		xData0 = geometry[0, 0, y]
		xData1 = geometry[0, 1, y]
		xData2 = geometry[0, 2, y]
		xData3 = geometry[0, 3, y]
		anglesData = geometry[0, 4, y]

		# loop over the number of columns
		for x in range(0, numCols):
			# if our score does not have sufficient probability, ignore it
			if scoresData[x] < 0.5:
				continue
	 
			# compute the offset factor as our resulting feature maps will
			# be 4x smaller than the input image
			(offsetX, offsetY) = (x * 4.0, y * 4.0)
	 
			# extract the rotation angle for the prediction and then
			# compute the sin and cosine
			angle = anglesData[x]
			cos = np.cos(angle)
			sin = np.sin(angle)
	 
			# use the geometry volume to derive the width and height of
			# the bounding box
			h = xData0[x] + xData2[x]
			w = xData1[x] + xData3[x]
	 
			# compute both the starting and ending (x, y)-coordinates for
			# the text prediction bounding box
			endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
			endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
			startX = int(endX - w)
			startY = int(endY - h)
	 
			# add the bounding box coordinates and probability score to
			# our respective lists
			rects.append((startX, startY, endX, endY))
			confidences.append(scoresData[x])

	# apply non-maxima suppression to suppress weak, overlapping bounding
	# boxes
	boxes = non_max_suppression(np.array(rects), probs=confidences)


	height, width, channels = orig.shape
	img = np.zeros([height,width,1],dtype=np.uint8)
	#orig.fill(0) 

	# loop over the bounding boxes
	for (startX, startY, endX, endY) in boxes:
		# scale the bounding box coordinates based on the respective
		# ratios
		startX = int(startX * rW)
		startY = int(startY * rH)
		endX = int(endX * rW)
		endY = int(endY * rH)
	 
		# draw the bounding box on the image
		cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)
		cv2.rectangle(img, (startX, startY), (endX, endY), (255,255,255), -1)


	#percentuale del text all'interno di un'immagine
	nonzero = cv2.countNonZero(img)
	total = width * height
	ratio = nonzero * 100 / float(total)
	#print(ratio)

	# show the output image
	#cv2.imshow("Text Detection", orig)
	#cv2.imshow("Text Detection BW", img)
	#cv2.waitKey(0)
	return ratio

def get_text_density(videoId):
	t = []
	if os.path.exists(frames_dir.format(videoId)):
		for file in os.listdir(frames_dir.format(videoId)):
			if file.endswith(".bmp"):
				image_path = os.path.join(frames_dir.format(videoId), file)
				t.append(get_text_density_frame(image_path))
	mean = (statistics.mean(t) if t else 'None')
	return mean