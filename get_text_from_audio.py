import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
import time
import csv
import json

import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import operator

OUTPUT_FILE = "data\\dataset_text_analysis_.csv"
INPUT_FILE = "data\\dataset.csv"
path_audios="D:\\ProgettoMLSII\\audios\{}\\"
name_file_audio = "D:\\ProgettoMLSII\\audios\\{}\\{}_temp.wav"
name_frame_file_audio = "D:\\ProgettoMLSII\\audios\\{}\\{}_frame\\{}_{}.wav"
path_frames_audio = "D:\\ProgettoMLSII\\audios\\{}\\{}_frame\\"

def get_text(videoId):
	path_audio = name_file_audio.format(videoId,videoId)
	if  os.path.exists(path_audio):
		if not os.path.exists((path_frames_audio.format(videoId, videoId)+"text.txt")):
			file = create_folder_file(videoId)
			create_frame_audio(path_audio, videoId)
			text(videoId, file)
		return get_analisi_testo((path_frames_audio.format(videoId, videoId)+"text.txt"))



def create_folder_file(videoId):
	if not os.path.exists(path_frames_audio.format(videoId, videoId)):
		t = path_frames_audio.format(videoId, videoId)
		print(t)
		os.mkdir(path_frames_audio.format(videoId, videoId)) 
	file = open((path_frames_audio.format(videoId, videoId)+"text.txt"),"w")
	return file

def create_frame_audio(path_audio, videoId):
	file_audio = AudioSegment.from_file(path_audio)
	frame_length_ms = 60000 # pydub calculates in millisec
	frames = make_chunks(file_audio, frame_length_ms)
	for i, chunk in enumerate(frames):
		chunk_name = name_frame_file_audio.format(videoId,videoId,videoId,i)
		print ("exporting", chunk_name)
		chunk.export(chunk_name, format="wav")

def text (videoId, file):
	i = 0
	for frame in os.listdir(path_frames_audio.format(videoId, videoId)): 
		if frame.endswith(".wav"):
			r=sr.Recognizer()
			path_frame=name_frame_file_audio.format(videoId, videoId, videoId, i)
			print(i, sep=' ', end='', flush=True)
			i=i+1
			with sr.AudioFile(path_frame) as source:
				audio = r.record(source)
			try:
				text = r.recognize_google(audio)
				file.write(text)
			except Exception as e:
				print(e)
	file.close() 

def get_analisi_testo(path_text):
#if __name__ == '__main__':
	f = open(path_text, "r") 
	input=f.read()
	tokenized_word=word_tokenize(input)
	stop_words=set(stopwords.words("english"))
	ciccia=['I', '\'s', 'one', 'and','I','A','And','So','arnt','This', 'way' 'also','When','It','many','Many','so','cant','Yes','yes','No','no','These','these', ',']
	stop_words.update(ciccia)
	tokenized_sent = tokenized_word
	filtered_sent=[]
	for w in tokenized_sent:
		if w not in stop_words:
			filtered_sent.append(w)
	fdist = FreqDist(filtered_sent)
	mappa = sorted(fdist.items(), key=operator.itemgetter(1), reverse=True)

	s= '{'
	#print(json.dumps(mappa, ensure_ascii=False))
	for key,val in mappa:

		vall= str(val)+','
		s+=key+':'+vall
	if len(s) > 1 :
		s = s[:-1]
	s = s + '}'
	#print(s)
	return s


if __name__ == '__main__':
	start = time.time()
	with open(INPUT_FILE, encoding="utf8") as input , open(OUTPUT_FILE, 'w', newline='') as output:
		writer = csv.writer(output, delimiter=",")
		header = ['videoId','work frequency']
		writer.writerow(header)
		for row in csv.reader(input):
			if row[0] != 'videoId':
				print(f'Inizio testo at {time.strftime("%H:%M")}')
				results = []
				videoId = row[0].replace('/watch?v=','')
				result = get_text(videoId)
				element = [videoId, result]
				writer.writerow(element)
				print('scritto videoId = ', videoId)				

	print(' complete \n')
