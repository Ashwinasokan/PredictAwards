import scrapy
import json

class ReviewsSpider(scrapy.Spider):
    name = "spot"
    
    def start_requests(self):
		baseUrl = 'http://www.mrqe.com'
		with open('/home/ashwin/WorkBench/Dreams/ML/Scrapy/tutorial/search.json', 'r') as f:
			data = json.load(f)
			for datum in data:
				url = baseUrl + datum['link']
				request = scrapy.Request(url=url, callback=self.parse)
				request.meta['item'] = datum
				yield request

    def parse(self, response):
		datum = response.meta['item']
		for row in response.css('li.article'):
			critic = row.css('a.tooltip_container::text').extract_first()
			domain = row.css('span.source::text').extract_first()
			yield { 'Original_Title': datum['Original_Title'],
				'domain': domain,
				'critic': critic,
				'links': row.css("a.tooltip_container::attr(href)").extract_first() }
