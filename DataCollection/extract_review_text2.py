from csv import DictReader, DictWriter
import json
import webarticle2text
import os.path
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
baseUrl = 'http://www.mrqe.com'
progress = 0
p = open('progress.txt', 'r+',0)
for line in p:
	progress = int(line)
file_exists = os.path.isfile("/home/ashwin/WorkBench/Dreams/ML/Scrapy/tutorial/review2_text.csv")
o = DictWriter(open("/home/ashwin/WorkBench/Dreams/ML/Scrapy/tutorial/review2_text.csv", 'a',0), ["id","Original_Title", "domain","critic","link","text"])
if not file_exists:
	o.writeheader()
with open('/home/ashwin/WorkBench/Dreams/ML/Scrapy/tutorial/reviews2.csv', 'r') as f:
	reader = DictReader(f)
	for item in reader:
		if int(item['id']) <= progress:
			continue
		if item['link']:
			try:
				text = webarticle2text.extractFromURL(baseUrl+item['link'])
				if text:
					o.writerow({ 'Original_Title': item['Original_Title'],
					                    'id' : item['id'],
					                    'domain' : item['domain'],
										'link': item['link'],
										'text': text,
										'critic': item['critic'],})
			except:
				print(json.dumps(item, sort_keys=True,indent=2, separators=(',', ': ')))
				print(item['id'],baseUrl+item['link']," Unexpected error:", sys.exc_info()[0])
			progress = int(item['id'])
			p.write('{0}\n'.format(progress))
