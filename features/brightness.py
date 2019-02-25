import cv2
import os
import statistics

frames_dir = "frames\\{}\\"

def get_brightness_frame(image_path):
	image = cv2.imread(image_path)

	image_hsv = cv2.cvtColor(image,cv2.COLOR_RGB2HSV)
	h, s, v = cv2.split(image_hsv)
	brightness = v.mean()
	#print("Brightness medio dell'immagine: ", brightness)

	# show the images
	#cv2.imshow("Image", image)
	#cv2.imshow("Image HSV", image_hsv)
	#cv2.waitKey(0)

	return brightness


def get_brightness(videoId):
	b = []
	if os.path.exists(frames_dir.format(videoId)):
		for file in os.listdir(frames_dir.format(videoId)):
			if file.endswith(".bmp"):
				image_path = os.path.join(frames_dir.format(videoId), file)
				b.append(get_brightness_frame(image_path))
	return statistics.mean(b)
