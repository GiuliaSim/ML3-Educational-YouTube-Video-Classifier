import scipy.io.wavfile as wav
from scipy.io.wavfile import _read_riff_chunk
import numpy as np
import speechpy
import os
import time
import concurrent.futures
import csv
from os.path import getsize
from pprint import pprint

INPUT_FILE = "data\\dataset.csv"
audios_dir = "audios\\"
name_file_audio = "{}\\{}_temp.wav"

def format_time(start,end):
	minutes, seconds = divmod(end - start, 60) 
	execut_time = "{:0>2}:{:05.2f}".format(int(minutes),seconds)
	return execut_time

def get_features(row):
	if row[0] != 'videoId':
		videoId = row[0].replace('/watch?v=','')
		file_name = name_file_audio.format(audios_dir,videoId)
		if os.path.isfile(file_name):
			print(f'Process {os.getpid()} working record {videoId} at {time.strftime("%H:%M")}')

			fs, signal = wav.read(file_name)
			signal = signal[:,0]

			# Example of pre-emphasizing:
			# Preemphasising on the signal.
			# This is a preprocessing step.
			signal_preemphasized = speechpy.processing.preemphasis(signal, cof=0.98)

			# Example of staching frames: 
			# Create stacking frames from the raw signal.
			frames = speechpy.processing.stack_frames(signal, sampling_frequency=fs, frame_length=0.020, frame_stride=0.01, filter=lambda x: np.ones((x,)),
			         zero_padding=True)

			# Example of FFT Spectrum:
			# Calculation of the Fast Fourier Transform.
			fft_spectrum = speechpy.processing.fft_spectrum(frames, fft_points=512)
			#print('Fast Fourier Transform=', fft_spectrum.shape)

			# Example of extracting power spectrum:
			# Power Spectrum calculation.
			power_spectrum = speechpy.processing.power_spectrum(frames, fft_points=512)
			#print('power spectrum shape=', power_spectrum.shape)

			# Example of extracting log power spectrum:
			# Log Power Spectrum calculation.
			log_power_spectrum = speechpy.processing.log_power_spectrum(frames, fft_points=512, normalize=True)
			#print('log power spectrum shape=', log_power_spectrum.shape)

			############# Extract MFCC features #############
			mfcc = speechpy.feature.mfcc(signal, sampling_frequency=fs, frame_length=0.020, frame_stride=0.01,
			             num_cepstral=13, num_filters=40, fft_length=512, low_frequency=0, high_frequency=None)
			
			mfcc_cmvn = speechpy.processing.cmvn(mfcc,variance_normalization=True)
			#print('mfcc(mean + variance normalized) feature shape=', mfcc_cmvn.shape)

			mfcc_cmvnw = speechpy.processing.cmvnw(mfcc,win_size=301,variance_normalization=True)
			#print('mfcc(mean + variance normalized) over the sliding window feature shape=', mfcc_cmvnw.shape)

			mfcc_feature_cube = speechpy.feature.extract_derivative_feature(mfcc)
			#print('mfcc feature cube shape=', mfcc_feature_cube.shape)

			############# Extract logenergy features #############
			logenergy = speechpy.feature.lmfe(signal, sampling_frequency=fs, frame_length=0.020, frame_stride=0.01,
			             num_filters=40, fft_length=512, low_frequency=0, high_frequency=None)
			logenergy_feature_cube = speechpy.feature.extract_derivative_feature(logenergy)
			#print('logenergy features=', logenergy.shape)

			print(f'Process {os.getpid()} done procesing record {videoId} at {time.strftime("%H:%M")}')

			return {
				'videoId': videoId,
				'fft_spectrum': fft_spectrum.shape,
				'power_spectrum': power_spectrum.shape,
				'log_power_spectrum': log_power_spectrum.shape,
				'mfcc': mfcc.shape,
				'cmvn': mfcc_cmvn.shape,
				'cmvnw': mfcc_cmvnw.shape,
				'mfcc_feature_cube_shape': mfcc_feature_cube.shape,
				'logenergy_features': logenergy.shape
			}
		return {'videoId':videoId}

if __name__ == '__main__':
	start = time.time()
	with open(INPUT_FILE, encoding="utf8") as input:
		with concurrent.futures.ThreadPoolExecutor() as executor:
			result = executor.map(get_features, csv.reader(input))
	end = time.time()

	pprint(tuple(result))
	print(f'\nTime to complete: {format_time(start, end)}\n')	

# if __name__ == '__main__':
# 	start = time.time()
# 	with open(INPUT_FILE, encoding="utf8") as input:
# 		count = 1
# 		for row in csv.reader(input):
# 			if count < 4 and row[0] != 'videoId':
# 				videoId = row[0].replace('/watch?v=','')
# 				get_features(videoId)
# 				count += 1
# 	end = time.time()
# 	print(f'\nTime to complete: {format_time(start, end)}\n')	