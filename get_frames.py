import cv2
import os
import csv
import collections
import concurrent.futures

INPUT_FILE = "data\\dataset.csv"
url = 'https://www.youtube.com/watch?v={}'
name_file_vieo = "video_temp\\{}_temp.mp4"
#name_file_vieo = "{}_temp.mp4"
frames_dir = "frames\\{}\\"
frame_name = "{}{}.bmp"

def get_frames(row):
	if row[0] != 'videoId':
		videoId = row[0].replace('/watch?v=','')
		print(f'Process {os.getpid()} working record {videoId}')
		#download del video
		#os.system("youtube-dl -f worst " + url.format(videoId) + " -o " + name_file_vieo)
		os.system("youtube-dl  " + url.format(videoId) + " -o " + name_file_vieo.format(videoId))

		#creazione della folder dove verranno inseriti i frames
		if not os.path.exists(frames_dir.format(videoId)):
				os.makedirs(frames_dir.format(videoId))

		#start the video
		cap = cv2.VideoCapture(name_file_vieo.format(videoId))
		count = 0
		success = True

		print (videoId + ': Inizio recupero frames')
		while success:
			cap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))
			success,frame = cap.read()
			if frame is None:
				break

			#print ('Read a new frame: ', success)

			cv2.imwrite(frames_dir.format(videoId) + frame_name.format(videoId,count), frame)
			
			#salva un frame ogni 5 secondi
			count = count + 5  

		cap.release()

		#il video viene eliminato
		if os.path.exists(name_file_vieo.format(videoId)):
			os.remove(name_file_vieo.format(videoId))
		
		print(f'Process {os.getpid()} done procesing record {videoId}')
		return True


if __name__ == '__main__':
	with open(INPUT_FILE, encoding="utf8") as input:
		with concurrent.futures.ThreadPoolExecutor() as executor:
			#creazione della folder dove verranno inseriti i frames
			if not os.path.exists("video_temp"):
				os.makedirs("video_temp")
			result = executor.map(get_frames, csv.reader(input))
