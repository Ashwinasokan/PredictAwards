from csv import DictReader, DictWriter
from collections import Counter
X = []
Y = []
reader = DictReader(open("picture.csv", 'r'))
for idx,row in enumerate(reader):
	if idx > 400 and row['win'] == '0':
		continue;
	Y.append(row['win'])
	del row['win']
	X.append(row)
print Counter(Y)
print len(X)
