# grocery_spider.py
import scrapy

class GrocerySpider(scrapy.Spider):
    name = "grocery"
    start_urls = ["https://www.target.com/c/grocery/-/N-5xt1a"]

    def parse(self, response):
        for product in response.css('.product-item'):
            yield {
                'category_name': product.css('.category::text').get(default='Groceries'),
                'price': product.css('.price::text').re_first(r'[\d\.]+'),
                'source': 'Regional Supermarket'
            }