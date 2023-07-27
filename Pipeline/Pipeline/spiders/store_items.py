import scrapy
import math

class StoreItemsSpider(scrapy.Spider):
    name = 'store_items'
    start_urls = ['https://jolse.com/category/skincare/1018/?page=1', 'https://jolse.com/category/makeup/1036/?page=1', 'https://jolse.com/category/hair-body/1060/?page=1', 'https://jolse.com/category/devices-tools/1184/?page=1',]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(StoreItemsSpider, cls).from_crawler(crawler, *args, **kwargs)
        return spider

    def parse(self, response):
        url_without_page = response.url[:-1]
        num_items = int(response.xpath('//p[@class="prdCount"]/strong/text()').get())
        numpages = math.ceil(num_items / 20)

        urls = []
        for i in range(1, numpages):
            urls.append(url_without_page + str(i))
            yield response.follow(url_without_page + str(i), callback=self.parseItem)

    def parseItem(self, response):
        items = response.xpath('(//ul[@class="prdList grid5"])[2]/li[@class="xans-record-"]')
        for item in items:
            name = item.xpath('.//a/span[@style="font-size:14px;color:#555555;font-weight:bold;"]/text()').get()
            original_price = item.xpath('.//span[@style="font-size:16px;color:#888888;text-decoration:line-through;"]/text()').get()
            if not original_price:
                original_price = item.xpath('.//li[@class=" xans-record-"]/span[@style="font-size:16px;color:#888888;"]/text()').get()
            sale_price = item.xpath('.//span[@style="font-size:20px;color:#ff2d46;font-weight:bold;"]/text()').get()
            img = item.xpath('.//a/img/@src').get()

            if not sale_price:
                sale_price = original_price

            sale_price = sale_price.replace(',', "")
            original_price = original_price.replace(',', "")

            yield {"name": name, "original_price": float(original_price[4:]), "sale_price": float(sale_price[4:]), "img": img}