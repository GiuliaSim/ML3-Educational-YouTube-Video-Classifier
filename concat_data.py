import pandas as pd


#New data
NEW_DATA_FILE = 'data\\edu_videos_final.csv'
OLD_DATA_FILE = 'data\\old_data_final.csv'
OUTPUT_FILE = 'data\\dataset.csv'

a = pd.read_csv(NEW_DATA_FILE)
b = pd.read_csv(OLD_DATA_FILE)
result = pd.concat([a,b])
result.to_csv(OUTPUT_FILE, index=False)