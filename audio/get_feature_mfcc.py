import scipy.io.wavfile as wav
from scipy.fftpack import fft
from scipy.signal import butter, lfilter
import numpy as np
import speechpy
import os
import time
import csv
from os.path import getsize
import json
import collections
import matplotlib.pyplot as plt

INPUT_FILE = "..\\data\\dataset2.csv"
OUTPUT_FILE = "..\\data\\dataset_audio_mfcc.csv"
audios_dir = "..\\audios"
name_file_audio = "{}\\{}\\{}_temp.wav"
lo_filter,hi_filter = 85,255
pre_emphasis = 0.97

def format_time(start,end):
	minutes, seconds = divmod(end - start, 60) 
	execut_time = "{:0>2}:{:05.2f}".format(int(minutes),seconds)
	return execut_time
def get_mfcc(fs, signal):
	length, channels = (len(signal), 1) if len(signal.shape) == 1 else signal.shape

	if channels > 1:
			signal = signal[:,0]
		
	# Preemphasising on the signal.
	# This is a preprocessing step.
	#signal_preemphasized = speechpy.processing.preemphasis(signal, cof=0.98)

	# Create stacking frames from the raw signal.
	frames = speechpy.processing.stack_frames(signal, sampling_frequency=fs, frame_length=0.020, frame_stride=0.01, filter=lambda x: np.ones((x,)),
			 zero_padding=True)

	############# Extract MFCC features #############
	mfcc = speechpy.feature.mfcc(signal, sampling_frequency=fs, frame_length=0.020, frame_stride=0.01,
				 num_cepstral=13, num_filters=40, fft_length=512, low_frequency=0, high_frequency=None)

	#viene calcolato il valore medio di ogni coefficiente 
	i_vector = mfcc.mean(0)
	i_vector_str = np.array2string(i_vector, separator=',', max_line_width=np.inf)
	
	return (mfcc, i_vector_str)

def get_features(videoId):
	file_name = name_file_audio.format(audios_dir,videoId,videoId)
	print(os.path.isfile(file_name))
	if os.path.isfile(file_name):
		print(f'Working record {videoId} at {time.strftime("%H:%M")}')

		fs, signal = wav.read(file_name)

		mfcc, i_vector_str = get_mfcc(fs, signal)
		print(f'Fine mfcc at {time.strftime("%H:%M")}')
		
		print(f'Done procesing record {videoId} at {time.strftime("%H:%M")}')

		return {
			'videoId': videoId,
			'mfcc_shape': mfcc.shape,
			'mfcc_mean': i_vector_str
		}
	return {'videoId':videoId}


if __name__ == '__main__':
	start = time.time()
	
	with open(INPUT_FILE, encoding="utf8") as input, open(OUTPUT_FILE, 'w+', newline='') as output:
		count = 1
		writer = csv.writer(output)
		writer.writerow(['videoId','mfcc_shape', 'mfcc_mean'])
		for row in csv.reader(input):
			if row[0] != 'videoId':
				videoId = row[0].replace('/watch?v=','')
				results = []
				result = get_features(videoId)
				results.append(result)
				data_str = json.dumps(tuple(results))
				data_audio = json.loads(data_str)
				print(result)
				for elem in data_audio:
					if elem is not None:
						writer.writerow(elem.values())


		

