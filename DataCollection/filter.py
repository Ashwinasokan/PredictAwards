import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# List to hold dictionaries
awards_map = dict()
reviews_map = dict()
def getReviewsCount(item):
	return item[1]
# Iterate through each row in worksheet and fetch values into dict

with open('Academy_Awards_2006.csv', 'rb') as csvfile:
	awardreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row_values in awardreader:
		original_title = (row_values[0]).strip().lower()
		category = (row_values[5]).lower().replace(" ", "")
		winner = (row_values[6]).lower().replace(" ", "")
		if 'cinematography' in category:
			if winner == 'x':
				awards_map[original_title] = 1
			else:
				awards_map[original_title] = 0

with open('reviews.csv', 'rb') as csvfile:
	reviewreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row_values in reviewreader:
		original_title = (row_values[1]).strip().lower()
		text = (row_values[5]).strip().lower()
		if original_title in awards_map:
			if original_title not in reviews_map:
				reviews_map[original_title] = set()
			reviews_map[original_title].add(text)
			
print(len(reviews_map))
print(len(awards_map))
positives = []
negatives = []
selected = []
for k,v in awards_map.items():
	if v == 1 and k in reviews_map:
		positives.append((k,len(reviews_map[k])))
		selected.append(k)
	elif v == 0 and k in reviews_map:
		negatives.append((k,len(reviews_map[k])))
negatives = sorted(negatives,key=getReviewsCount,reverse=True)
count = len(selected)-1
while count>=0:
	selected.append(negatives[count][0])
	count -= 1
print(len(selected))
o = csv.DictWriter(open("best_cinematography.csv", 'w'), ["original_title", "winner","reviews_count","text"])
o.writeheader()
for k,v in awards_map.items():
	if k in reviews_map and k in selected:
		d = {'original_title': k, 'winner': v,'reviews_count': len(reviews_map[k]), 'text': ' '.join(reviews_map[k])}
		o.writerow(d)
