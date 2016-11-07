import scrapy
import json
import re
from collections import OrderedDict

class QuotesSpider(scrapy.Spider):
    name = "single"
    
    def start_requests(self):
		datum = OrderedDict()
		datum['Original_Title'] = 'The Pickwick Papers'
		datum['Year'] = '1955'
		baseUrl = 'https://www.rottentomatoes.com/search/?search='
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
		results = []
		for row in response.css('li.bottom_divider.clearfix'):
			self.logger.info('Fuck %s', row.css("span.movie_year::text").extract_first())
			yr = re.sub('[^0-9]','',row.css("span.movie_year::text").extract_first())
			if yr in years:
				results.append(row.css("div.bold a::attr(href)").extract_first())
				break
		if not results:
			for row in response.css('li.bottom_divider.clearfix'):
				yr = re.sub('[^0-9]','',row.css("span.movie_year::text").extract_first())
				for y in years:
					self.logger.info('What %s %s', y,yr)
					diff = int(y)-int(yr)
					if diff > 0 and diff < 5:
						results.append(row.css("div.bold a::attr(href)").extract_first())
						break
				if results:
					break
		for result in results:
			yield { 'Original_Title': datum['Original_Title'],
					'link': result,}

