import csv
import requests

INPUT_FILE = 'D:\\giuly\\Desktop\\Progetto ML3 YouTube\\ML5-MINERVA-EducationaVideosClassifier-master\\dataset.csv'
OUTPUT_FILE = 'data\\video.csv'
url = 'https://www.youtube.com/watch?v={}'

with open(INPUT_FILE) as input:
     for row in csv.reader(input):
        videoId = row[0]
        page = url.format(videoId)
        request = requests.get(page)
        if request.status_code == 200:
            print(page)
            print(row[17])