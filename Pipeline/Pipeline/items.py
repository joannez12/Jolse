# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class CrawlItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    original_price = scrapy.Field()
    sale_price = scrapy.Field()
    img = scrapy.Field()
