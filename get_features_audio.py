import scipy.io.wavfile as wav
from scipy.fftpack import fft
from scipy.signal import butter, lfilter
import numpy as np
import speechpy
import os
import time
import concurrent.futures
import csv
from os.path import getsize
from pprint import pprint
import json
import collections
import matplotlib.pyplot as plt

INPUT_FILE = "data\\dataset.csv"
OUTPUT_FILE = "data\\dataset_audio.csv"
audios_dir = "audios\\"
name_file_audio = "{}\\{}_temp.wav"
lo_filter,hi_filter = 85,255
#lo_filter,hi_filter = 0.25,0.75
pre_emphasis = 0.97

def format_time(start,end):
	minutes, seconds = divmod(end - start, 60) 
	execut_time = "{:0>2}:{:05.2f}".format(int(minutes),seconds)
	return execut_time

def get_frequencies(fs, signal):
	length, channels = (len(signal), 1) if len(signal.shape) == 1 else signal.shape
	type_signal = signal.dtype
	dt = 1/float(fs)

	#Filtri 
	b_band,a_band = butter(N=1, Wn=[lo_filter/(fs/2), hi_filter/(fs/2)], btype='band')
	b_high,a_high = butter(N=1, Wn=hi_filter/(fs/2), btype='highpass')
	b_low,a_low = butter(N=1, Wn=lo_filter/(fs/2), btype='lowpass')
	
	if channels == 2:
		left, right = signal[:,0], signal[:,1]
		#left = np.append(left[0], left[1:] - pre_emphasis * left[:-1])
		#right = np.append(right[0], right[1:] - pre_emphasis * right[:-1])
		lf, rf = abs(fft(left)), abs(fft(right))
		
		vf_l, vf_r = lfilter(b_band,a_band,lf), lfilter(b_band,a_band,rf)
		#not_nan_val = np.count_nonzero(~np.isnan(vf_lf)) #numero dei valori not nan all'interno di x
		#vf_lf = vf_lf[~np.isnan(vf_lf)] #elimina i valori nan
		#vf_lf = vf_lf[0:(not_nan_val-1)] #elimina l'ultimo valore dell'array perchè pari a -inf
		voice_frequencies = (vf_l.mean() + vf_r.mean()) / 2.

		filtered_l, filtered_r = lfilter(b_high,a_high,lf), lfilter(b_high,a_high,rf)
		nvf_l, nvf_r = lfilter(b_low,a_low,filtered_l), lfilter(b_low,a_low,filtered_r)
		non_voice_frequencies = (nvf_l.mean() + nvf_r.mean()) / 2.
	else:
		#signal = np.append(signal[0], signal[1:] - pre_emphasis * signal[:-1])
		signalf = abs(fft(signal))

		vf_signal = lfilter(b_band,a_band,signalf)
		voice_frequencies = vf_signal.mean()

		filtered_signal = lfilter(b_high,a_high,signalf)
		nvf_signal = lfilter(b_low,a_low,filtered_signal)
		non_voice_frequencies = nvf_signal.mean()
	return (voice_frequencies, non_voice_frequencies)

def get_mfcc(signal):
	length, channels = (len(signal), 1) if len(signal.shape) == 1 else signal.shape

	if channels > 1:
			signal = signal[:,0]
		
	# Example of pre-emphasizing:
	# Preemphasising on the signal.
	# This is a preprocessing step.
	#signal_preemphasized = speechpy.processing.preemphasis(signal, cof=0.98)

	# Example of staching frames: 
	# Create stacking frames from the raw signal.
	frames = speechpy.processing.stack_frames(signal, sampling_frequency=fs, frame_length=0.020, frame_stride=0.01, filter=lambda x: np.ones((x,)),
			 zero_padding=True)

	# Example of FFT Spectrum:
	# Calculation of the Fast Fourier Transform.
	#fft_spectrum = speechpy.processing.fft_spectrum(frames, fft_points=512)
	#print('Fast Fourier Transform=', fft_spectrum.shape)

	# Example of extracting power spectrum:
	# Power Spectrum calculation.
	#power_spectrum = speechpy.processing.power_spectrum(frames, fft_points=512)
	#print('power spectrum shape=', power_spectrum.shape)

	# Example of extracting log power spectrum:
	# Log Power Spectrum calculation.
	#log_power_spectrum = speechpy.processing.log_power_spectrum(frames, fft_points=512, normalize=True)
	#print('log power spectrum shape=', log_power_spectrum.shape)

	############# Extract MFCC features #############
	mfcc = speechpy.feature.mfcc(signal, sampling_frequency=fs, frame_length=0.020, frame_stride=0.01,
				 num_cepstral=13, num_filters=40, fft_length=512, low_frequency=0, high_frequency=None)

	#viene calcolato il valore medio di ogni coefficiente 
	i_vector = mfcc.mean(0)
	i_vector_str = np.array2string(i_vector, separator=',', max_line_width=np.inf)
	
	#mfcc_cmvn = speechpy.processing.cmvn(mfcc,variance_normalization=True)
	#print('mfcc(mean + variance normalized) feature shape=', mfcc_cmvn.shape)

	#mfcc_cmvnw = speechpy.processing.cmvnw(mfcc,win_size=301,variance_normalization=True)
	#print('mfcc(mean + variance normalized) over the sliding window feature shape=', mfcc_cmvnw.shape)

	#mfcc_feature_cube = speechpy.feature.extract_derivative_feature(mfcc)
	#print('mfcc feature cube shape=', mfcc_feature_cube.shape)

	############# Extract logenergy features #############
	#logenergy = speechpy.feature.lmfe(signal, sampling_frequency=fs, frame_length=0.020, frame_stride=0.01,
	#             num_filters=40, fft_length=512, low_frequency=0, high_frequency=None)
	#logenergy_feature_cube = speechpy.feature.extract_derivative_feature(logenergy)
	#print('logenergy features=', logenergy.shape)
	return (mfcc, i_vector_str)

def get_features(videoId):
	#if row[0] != 'videoId':
		#videoId = row[0].replace('/watch?v=','')
	file_name = name_file_audio.format(audios_dir,videoId)
	if os.path.isfile(file_name):
		print(f'Process {os.getpid()} working record {videoId} at {time.strftime("%H:%M")}')

		fs, signal = wav.read(file_name)

		voice_frequencies, non_voice_frequencies = get_frequencies(fs, signal)
		print(f'Fine frequencies at {time.strftime("%H:%M")}')

		mfcc, i_vector_str = get_mfcc(fs, signal)
		print(f'Fine mfcc at {time.strftime("%H:%M")}')
		
		print(f'Process {os.getpid()} done procesing record {videoId} at {time.strftime("%H:%M")}')

		return {
			'videoId': videoId,
			'voice_frequencies': voice_frequencies,
			'non_voice_frequencies': non_voice_frequencies,
			#'fft_spectrum': fft_spectrum.shape,
			#'power_spectrum': power_spectrum.shape,
			#'log_power_spectrum': log_power_spectrum.shape,
			'mfcc_shape': mfcc.shape,
			'mfcc_mean': i_vector_str
			#'mfcc_cmvn': mfcc_cmvn.shape,
			#'mfcc_cmvnw': mfcc_cmvnw.shape,
			#'mfcc_feature_cube_shape': mfcc_feature_cube.shape,
			#'logenergy_features': logenergy.shape
		}
	return {'videoId':videoId}

# if __name__ == '__main__':
# 	start = time.time()
# 	with open(INPUT_FILE, encoding="utf8") as input:
# 		with concurrent.futures.ThreadPoolExecutor() as executor:
# 			result = executor.map(get_features, csv.reader(input))
# 	end = time.time()

# 	#pprint(tuple(result))
# 	print(f'\nTime to complete: {format_time(start, end)}\n')

# 	data_str = json.dumps(tuple(result))
# 	data_audio = json.loads(data_str)	

# 	#salva il risultato in un file csv
# 	with open(OUTPUT_FILE, 'w', newline='') as output:
# 		writer = csv.writer(output)
# 		count = 0
# 		for elem in data_audio:
# 			if elem is not None:
# 				if count == 0:
# 					header = elem.keys()
# 					writer.writerow(header)
# 					count += 1
# 				writer.writerow(elem.values())
# 				#writer.writerow(elem)
# 		print(f'Result saved in: {OUTPUT_FILE}')

if __name__ == '__main__':
	start = time.time()
	results = []
	with open(INPUT_FILE, encoding="utf8") as input:
		count = 1
		for row in csv.reader(input):
			if row[0] != 'videoId':
				videoId = row[0].replace('/watch?v=','')
				result = get_features(videoId)
				results.append(result)
				#print(result)
				count += 1
	end = time.time()
	print(f'\nTime to complete: {format_time(start, end)}\n')

	data_str = json.dumps(tuple(results))
	data_audio = json.loads(data_str)	

	#salva il risultato in un file csv
	with open(OUTPUT_FILE, 'w', newline='') as output:
		writer = csv.writer(output)
		count = 0
		for elem in data_audio:
			if elem is not None:
				if count == 0:
					header = elem.keys()
					writer.writerow(header)
					count += 1
				writer.writerow(elem.values())
				#writer.writerow(elem)
		print(f'Result saved in: {OUTPUT_FILE}')