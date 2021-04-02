import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import MmyfirstItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class MmyfirstSpider(scrapy.Spider):
	name = 'myfirst'
	start_urls = ['https://www.myfirst.bank/coronavirus-news-and-resources']

	def parse(self, response):
		post_links = response.xpath('//h2/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = "Date is not stated in article"
		title = response.xpath('//h1/span/text()').get()
		if not title:
			title = response.xpath('//h2/text()').get()
		content = response.xpath('//div[@class="blog-detail"]/div[1]//text() |//div[@id="Content_C017_Col00"]//div[@class="sfContentBlock sf-Long-text"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=MmyfirstItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
