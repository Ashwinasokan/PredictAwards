from csv import DictReader, DictWriter
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
o = DictWriter(open("/home/ashwin/WorkBench/Dreams/ML/Scrapy/tutorial/reviews2.csv", 'w'), ["id","Original_Title", "domain","critic","link"])
o.writeheader()
with open('/home/ashwin/WorkBench/Dreams/ML/Scrapy/tutorial/reviews2.json', 'r') as f:
	data = json.load(f)
	for idx, item in enumerate(data):
		o.writerow({ 'Original_Title': item['Original_Title'],
					    'domain' : item['domain'],
						'link': item['links'],
						'critic': item['critic'],
						'id':idx,})

