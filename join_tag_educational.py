import pandas as pd

#Old data
#UPDATE_DATA_FILE = 'data\\old_data_update.csv'
#OLD_DATA_FILE = 'D:\\giuly\\Desktop\\Progetto ML3 YouTube\\ML5-MINERVA-EducationaVideosClassifier-master\\dataset.csv'
#OUTPUT_FILE = 'data\\old_data_final.csv'

#New data
UPDATE_DATA_FILE = 'data\\edu_videos_update.csv'
OLD_DATA_FILE = 'data\\edu_videos_tag.csv'
OUTPUT_FILE = 'data\\edu_videos_final.csv'

a = pd.read_csv(UPDATE_DATA_FILE)
b = pd.read_csv(OLD_DATA_FILE)
merged = a.merge(b[['videoId','IsEducational']], on='videoId', how='left')
merged.to_csv(OUTPUT_FILE, index=False)