import csv
import sys


NAME_FILE = sys.argv[1] 
INPUT_FILE = NAME_FILE + '.csv'
OUTPUT_FILE = NAME_FILE + '_clean.csv'

videosId = []

#remove empty row from csv and videoID duplicate
with open(INPUT_FILE) as input, open(OUTPUT_FILE, 'w', newline='') as output:
	writer = csv.writer(output)
	for row in csv.reader(input):
		if any(field.strip() for field in row):
			if row[0] not in videosId:
				videosId.append(row[0])
				writer.writerow(row)
