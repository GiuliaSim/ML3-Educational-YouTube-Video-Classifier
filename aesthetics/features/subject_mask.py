import cv2
import os
import statistics

frames_dir = "..\\..\\frames\\{}\\"

def get_subject_mask_frame(image_path):
	image = cv2.imread(image_path)

	height, width, channels = image.shape

	# initialize OpenCV's static fine grained saliency detector and
	# compute the saliency map
	saliency = cv2.saliency.StaticSaliencyFineGrained_create()
	(success, saliencyMap) = saliency.computeSaliency(image)
	saliencyMap = (saliencyMap * 10).astype("uint8")

	# if we would like a *binary* map that we could process for contours,
	# compute convex hull's, extract bounding boxes, etc., we can
	# additionally threshold the saliency map
	threshMap = cv2.threshold(saliencyMap, 0, 255, cv2.THRESH_BINARY )[1]

	#percentuale del subject size all'interno di un'immagine
	nonzero = cv2.countNonZero(threshMap)
	total = width * height
	ratio = nonzero * 100 / float(total)
	#print(ratio)

	# show the images
	#cv2.imshow("Image", image)
	#cv2.imshow("Thresh", threshMap)
	#cv2.waitKey(0)
	return ratio

def get_subject_mask(videoId):
	s = []
	if os.path.exists(frames_dir.format(videoId)):
		for file in os.listdir(frames_dir.format(videoId)):
			if file.endswith(".bmp"):
				image_path = os.path.join(frames_dir.format(videoId), file)
				s.append(get_subject_mask_frame(image_path))
	
	mean = (statistics.mean(s) if s else 'None')
	return mean