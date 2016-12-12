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
person = 'Javier Bardem'
results = i.search_person(person)
print i.get_person_infoset()
print i.get_character_infoset()
for result in results:
	for key in result.keys():
		print (key,result[key])
