import scrapy
import json
import re

class QuotesSpider(scrapy.Spider):
    name = "search"
    
    def start_requests(self):
		baseUrl = 'http://www.mrqe.com/search?q='
		with open('/home/ashwin/WorkBench/Dreams/ML/Academy_Awards_2006.json', 'r') as f:
			data = json.load(f)
			for datum in data:
				url = baseUrl + datum['Original_Title']
				request = scrapy.Request(url=url, callback=self.parse)
				request.meta['item'] = datum
				yield request

    def parse(self, response):
		datum = response.meta['item']
		year = datum['Year']
		year.replace(" ", "")
		years = []
		if year.find('-')==-1:
			years.append(year)
		else:
			years = year.split("-")
		block = response.css('div.results')
		results = []
		for row in block.css('li'):
			yr = re.sub('[^0-9]','',row.css("a::text").extract_first())
			if not yr:
				continue
			if yr in years:
				results.append(row.css("a::attr(href)").extract_first())
				break
		if not results:
			for row in block.css('li'):
				yr = re.sub('[^0-9]','',row.css("a::text").extract_first())
				if not yr:
					continue
				for y in years:
					diff = int(y)-int(yr)
					if diff > 0 and diff < 5:
						results.append(row.css("a::attr(href)").extract_first())
						break
				if results:
					break
		for result in results:
			yield { 'Original_Title': datum['Original_Title'],
					'link': result,}

