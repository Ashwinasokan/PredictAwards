import imdb
import sys
from parse import *
from csv import DictReader, DictWriter
from sets import Set
from collections import OrderedDict
reload(sys)
sys.setdefaultencoding('utf8')
in_encoding = sys.stdin.encoding or sys.getdefaultencoding()
out_encoding = sys.stdout.encoding or sys.getdefaultencoding()
features = Set()
features.add('win')
movies_list = []
ignore = ['full-size cover url','long imdb title','long imdb canonical title','smart canonical title','smart long imdb canonical title',
'plot','kind','akas','imdbIndex','cover url','canonical title']
def encodeIt(it):
	return (u'%s' % (it)).encode(out_encoding, 'replace')
data = list(DictReader(open("input.csv", 'r')))
i = imdb.IMDb()
for idx, line in enumerate(data):
	category = line['Category'] 
	info = line['Additional Info']
	year = search('{:d} (', line['Year']).fixed[0]
	win = 1 if line['Won?'].strip() == 'YES' else 0
	if year < 50:
		year = year + 1900
	title = line['Nominee']
	if category == 'Actor -- Leading Role':
		extract = search('{} {', line['Additional Info'])
		if extract is None:
			print line
			continue;
		title = extract.fixed[0]
		found = False
		results = i.search_movie(title)
		for result in results:
			imdb_title = encodeIt(result['long imdb title'])
			r = search('({:d})', imdb_title)
			if r != None:
				diff = year - r.fixed[0]
				if diff >= 0 and diff < 5:
					movie = OrderedDict()
					i.update(result)
					i.update(result, info=('keywords','literature','locations'))
					for key in result.keys():
						if key in ignore:
							continue
						if type(result[key]) is list:
							for val in result[key]:
								if isinstance(val, (imdb.Person.Person,imdb.Company.Company)):
									val = key +'_'+ encodeIt(val['name'])
								else:
									val = key +'_'+ encodeIt(val)
								features.add(val)
								movie[val] = 1
						else:
							features.add(key)
							movie[key] = result[key]
					movie['win'] = win
					movies_list.append(movie)
					found = True
					break
		print (idx,title,year,found)
print(len(movies_list))
o = DictWriter(open("Actor.csv", 'w'), features)
o.writeheader()
for movie in movies_list:
        o.writerow(movie)
