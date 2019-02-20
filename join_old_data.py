import pandas as pd

UPDATE_DATA_FILE = 'D:\\giuly\\Desktop\\Progetto ML3 YouTube\\ML3-Educational-YouTube-Video-Classifier\\data\\old_data_update.csv'
OLD_DATA_FILE = 'D:\\giuly\\Desktop\\Progetto ML3 YouTube\\ML5-MINERVA-EducationaVideosClassifier-master\\dataset.csv'
OUTPUT_FILE = 'data\\final_old_data.csv'

a = pd.read_csv(UPDATE_DATA_FILE)
b = pd.read_csv(OLD_DATA_FILE)
merged = a.merge(b[['videoId','IsEducational']], on='videoId', how='left')
merged.to_csv(OUTPUT_FILE, index=False)