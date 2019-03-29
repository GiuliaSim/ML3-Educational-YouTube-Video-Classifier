import pandas as pd

DATA_FILE = 'all_dataset.csv'
OUTPUT_FILE = 'all_dataset.csv'

a = pd.read_csv(DATA_FILE)
a['IsEducational'] = a['IsEducational'].astype('bool')

a.to_csv(OUTPUT_FILE, index=False)