import pandas as pd

#Old data
#UPDATE_DATA_FILE = 'data\\old_data_update.csv'
#OLD_DATA_FILE = 'D:\\giuly\\Desktop\\Progetto ML3 YouTube\\ML5-MINERVA-EducationaVideosClassifier-master\\dataset.csv'
#OUTPUT_FILE = 'data\\old_data_final.csv'

#New data
DATA_BRIGHTNESS_FILE = 'dataset_aesthetic_brightness.csv'
DATA_ENTROPY_FILE = 'dataset_aesthetic_entropy.csv'
DATA_SUB_MASK_FILE = 'dataset_aesthetic_subject_mask.csv'
DATA_TEXT_DENSITY_FILE = 'dataset_aesthetic_text_density.csv'
DATA_SUB_CONTRAST_FILE = 'dataset_aesthetic_subject_contrast.csv'
DATA_BS_FILE = 'dataset_aesthetic_bs.csv'

OUTPUT_FILE = 'dataset_aesthetic.csv'

b = pd.read_csv(DATA_BRIGHTNESS_FILE)
e = pd.read_csv(DATA_ENTROPY_FILE)
t = pd.read_csv(DATA_TEXT_DENSITY_FILE)
s = pd.read_csv(DATA_SUB_MASK_FILE)
sc = pd.read_csv(DATA_SUB_CONTRAST_FILE)
bs = pd.read_csv(DATA_BS_FILE)
m = b.merge(e, on='videoId', how='left')
m = m.merge(t, on='videoId', how='left')
m = m.merge(s, on='videoId', how='left')
m = m.merge(sc, on='videoId', how='left')
m = m.merge(bs, on='videoId', how='left')

m.to_csv(OUTPUT_FILE, index=False)