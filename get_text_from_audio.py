import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks

path_audios="audios\{}\\"
name_file_audio = ".\\audios\\{}\\{}_temp.wav"
name_frame_file_audio = "audios\\{}\\{}_frame\\{}_{}.wav"
path_frames_audio = "audios\\{}\\{}_frame\\"

def get_text(videoId):
	path_audio = name_file_audio.format(videoId,videoId)
	file = create_folder_file(videoId)
	create_frame_audio(path_audio, videoId)
	text(videoId, file)

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
