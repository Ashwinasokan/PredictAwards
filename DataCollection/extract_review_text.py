from csv import DictReader, DictWriter
import json
import webarticle2text
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
baseUrl = 'http://www.mrqe.com'
o = DictWriter(open("/home/ashwin/WorkBench/Dreams/ML/Scrapy/tutorial/review_text.csv", 'w'), ["Original_Title", "critic","link","text"])
o.writeheader()
with open('/home/ashwin/WorkBench/Dreams/ML/Scrapy/tutorial/reviews.json', 'r') as f:
	data = json.load(f)
	for idx, item in enumerate(data):
		if item['links']:
			try:
				text = webarticle2text.extractFromURL(item['links'])
				if text:
					o.writerow({ 'Original_Title': item['Original_Title'],
										'link': item['links'],
										'text': text,
										'critic': item['critic'],})
			except:
				print(json.dumps(item, sort_keys=True,indent=2, separators=(',', ': ')))
				print(idx,item['links']," Unexpected error:", sys.exc_info()[0])
