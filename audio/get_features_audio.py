from pyfftw.interfaces.numpy_fft import fft
import scipy.io.wavfile as wav
from scipy.signal import butter, lfilter
import numpy as np
import os
import time
import csv

INPUT_FILE = "..\\data\\dataset.csv"
OUTPUT_FILE = "..\\data\\dataset_audio_freq.csv"
audios_dir = "..\\audios\\"
name_file_audio = "{}\\{}\\{}_temp.wav"
lo_filter,hi_filter = 85,255
pre_emphasis = 0.97

def format_time(start,end):
	hours, rem = divmod(end-start, 3600)
	minutes, seconds = divmod(rem, 60)
	execut_time = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
	return execut_time

def get_frequencies(fs, signal):
	length, channels = (len(signal), 1) if len(signal.shape) == 1 else signal.shape
	type_signal = signal.dtype
	#dt = 1/float(fs)

	#print(length,channels)

	#Filtri 
	b_band,a_band = butter(N=1, Wn=[lo_filter/(fs/2), hi_filter/(fs/2)], btype='band')
	b_high,a_high = butter(N=1, Wn=hi_filter/(fs/2), btype='highpass')
	b_low,a_low = butter(N=1, Wn=lo_filter/(fs/2), btype='lowpass')
	
	#print('Filtri creati')
	
	if channels == 2:
		left, right = signal[:,0], signal[:,1]
		#print('Segnale separato')
		#left = np.append(left[0], left[1:] - pre_emphasis * left[:-1])
		#right = np.append(right[0], right[1:] - pre_emphasis * right[:-1])
		
		lf, rf = fft(left), fft(right)
		#print('FFT eseguita')
		
		lf, rf = abs(lf), abs(rf)
		#print('ABS Eseguito')

		vf_l, vf_r = lfilter(b_band,a_band,lf), lfilter(b_band,a_band,rf)
		#print('Primo filtro applicato')
		#not_nan_val = np.count_nonzero(~np.isnan(vf_lf)) #numero dei valori not nan all'interno di x
		#vf_lf = vf_lf[~np.isnan(vf_lf)] #elimina i valori nan
		#vf_lf = vf_lf[0:(not_nan_val-1)] #elimina l'ultimo valore dell'array perchè pari a -inf
		voice_frequencies = (vf_l.mean() + vf_r.mean()) / 2.
		#print('voice_frequencies',voice_frequencies)

		filtered_l, filtered_r = lfilter(b_high,a_high,lf), lfilter(b_high,a_high,rf)
		#print('Secondo filtro applicato')
		nvf_l, nvf_r = lfilter(b_low,a_low,filtered_l), lfilter(b_low,a_low,filtered_r)
		#print('Terzo filtro applicato')
		non_voice_frequencies = (nvf_l.mean() + nvf_r.mean()) / 2.
		#print('non_voice_frequencies',non_voice_frequencies)
	else:
		#signal = np.append(signal[0], signal[1:] - pre_emphasis * signal[:-1])
		signalf = fft(signal)
		#print('FFT eseguita')
		
		signalf = abs(signalf)
		#print('ABS Eseguito')

		vf_signal = lfilter(b_band,a_band,signalf)
		#print('Primo filtro applicato')
		voice_frequencies = vf_signal.mean()
		#print('voice_frequencies',voice_frequencies)

		filtered_signal = lfilter(b_high,a_high,signalf)
		#print('Secondo filtro applicato')
		nvf_signal = lfilter(b_low,a_low,filtered_signal)
		#print('Terzo filtro applicato')
		non_voice_frequencies = nvf_signal.mean()
		#print('non_voice_frequencies',non_voice_frequencies)
	return (voice_frequencies, non_voice_frequencies)

def get_features(videoId):
	file_name = name_file_audio.format(audios_dir,videoId,videoId)
	if os.path.isfile(file_name):

		fs, signal = wav.read(file_name)

		voice_frequencies, non_voice_frequencies = get_frequencies(fs, signal)
		#print(f'Fine frequencies at {time.strftime("%H:%M")}')

		return {
			'videoId': videoId,
			'voice_frequencies': voice_frequencies,
			'non_voice_frequencies': non_voice_frequencies
		}
	return {'videoId':videoId}

if __name__ == '__main__':
	start = time.time()
	print(f'Start at {time.strftime("%H:%M")}')

	with open(INPUT_FILE, encoding="utf8") as input, open(OUTPUT_FILE, 'w', newline='') as output:
		writer = csv.writer(output)
		writer.writerow(['videoId','voice_frequencies','non_voice_frequencies'])

		count = 0
		for row in csv.reader(input):
			if row[0] != 'videoId':
				videoId = row[0].replace('/watch?v=','')
				print(f'[{videoId}] Inizio esecuzione..')
				result = get_features(videoId)
				voice_frequencies = 'None' if not 'voice_frequencies' in result else result['voice_frequencies']
				non_voice_frequencies = 'None' if not 'non_voice_frequencies' in result else result['non_voice_frequencies']
				print(f'[{videoId}] voice_frequencies: ',voice_frequencies)
				print(f'[{videoId}] non_voice_frequencies: ',non_voice_frequencies)
				writer.writerow([videoId,voice_frequencies,non_voice_frequencies])
				output.flush()
			count += 1

	end = time.time()
	print(f'End at {time.strftime("%H:%M")}')
	print('Done in', format_time(start, end))