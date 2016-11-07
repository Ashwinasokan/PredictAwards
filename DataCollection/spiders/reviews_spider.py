import scrapy
import json

class ReviewsSpider(scrapy.Spider):
    name = "reviews"
    
    def start_requests(self):
		baseUrl = 'https://www.rottentomatoes.com/'
		reviews = '/reviews/'
		with open('/home/ashwin/WorkBench/Dreams/ML/Scrapy/tutorial/quotes.json', 'r') as f:
			data = json.load(f)
			for datum in data:
				url = baseUrl + datum['link'] + reviews
				request = scrapy.Request(url=url, callback=self.parse)
				request.meta['item'] = datum
				yield request

    def parse(self, response):
		datum = response.meta['item']
		for row in response.css('div.review_table_row'):
			yield { 'Original_Title': datum['Original_Title'],
				'text': row.css("div.the_review::text").extract_first(),
				'critic': row.css("div.critic_name a::text").extract_first(),
				'links': row.css("div.subtle a::attr(href)").extract_first() }
