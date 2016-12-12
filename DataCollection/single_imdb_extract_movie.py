import imdb
import sys
from parse import *
from csv import DictReader, DictWriter
from sets import Set
from collections import OrderedDict
in_encoding = sys.stdin.encoding or sys.getdefaultencoding()
out_encoding = sys.stdout.encoding or sys.getdefaultencoding()
features = Set()
movies_list = []
ignore = ['full-size cover url','long imdb title','long imdb canonical title','smart canonical title','smart long imdb canonical title',
'plot','kind','akas','imdbIndex','cover url','canonical title']
i = imdb.IMDb()
year = 2010
title = 'The Fighter'
results = i.search_movie(title)
print i.get_movie_infoset()
for result in results:
	imdb_title = (u'%s' % (result['long imdb title'])).encode(out_encoding, 'replace')
	r = search('({:d})', imdb_title)
	if r != None:
		if year < 50:
			year = year + 1900
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
							val = key +'_'+ val['name']
						else:
							val = key +'_'+ val
						features.add(val)
						movie[val] = 1
				else:
					features.add(key)
					movie[key] = result[key]
			movies_list.append(movie)
			break
for movie in movies_list:
	for key in movie.keys():
		print (key,movie[key])
