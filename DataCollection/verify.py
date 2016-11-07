import json
from sets import Set
import collections
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
winnerCounter = collections.Counter()
loserCounter = collections.Counter()
target = open('result.txt', 'w')
with open('/home/ashwin/WorkBench/Dreams/ML/Academy_Awards_2006.json', 'r') as l:
	left = json.load(l)
	with open('/home/ashwin/WorkBench/Dreams/ML/Scrapy/tutorial/quotes.json', 'r') as r:
		S =  Set()
		right = json.load(r)
		for data in right:
			S.add(data['Original_Title'])
		for data in left:
			if data['Original_Title'] not in S:
				target.write(data['Original_Title'] + ','+ data['Year'] + '\n')
			else:
				if data['Winner?'] == 'X':
					winnerCounter[data['Category'].upper()] += 1
				else:
					loserCounter[data['Category'].upper()] += 1
		print (winnerCounter)
		print (loserCounter)
