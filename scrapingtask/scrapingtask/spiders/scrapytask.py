import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from ..items import ScrapingtaskItem


class LondonrelocationSpider(scrapy.Spider):
    name = 'londonrelocation'
    allowed_domains = ['londonrelocation.com']
    start_urls = ['https://londonrelocation.com/properties-to-rent/']

    def parse(self, response):
        for start_url in self.start_urls:
            yield Request(url=start_url,
                          callback=self.parse_area)

    def parse_area(self, response):
        area_urls = response.xpath('.//div[contains(@class,"area-box-pdh")]//h4/a/@href').extract()
        for area_url in area_urls:
            yield Request(url=area_url,
                          callback=self.parse_area_pages)

    def parse_area_pages(self, response):
        # Write your code here and remove `pass` in the following line
        for i in [1, 2]:
            page_number = response.url+'&pageset='+str(i)
            yield scrapy.Request(url=page_number,
                                 callback=self.page_scraping)


    def page_scraping(self, response):
        urls = ['https://londonrelocation.com' + url_property for url_property in response.css(".h4-space a::attr(href)").getall()]
        for url in urls :
            yield scrapy.Request(url=url,
                                 callback=self.property_scraping)

    def property_scraping(self,response):
        items = ScrapingtaskItem()
        title = response.css("h1::text").get()
        price = float(response.css("h3::text").get().split()[0][1:])
        url = response.url

        items['title'] = title
        items['price'] = price
        items['url'] = url

        yield items





        # an example for adding a property to the json list:
        # property = ItemLoader(item=Property())
        # property.add_value('title', '2 bedroom flat for rental')
        # property.add_value('price', '1680') # 420 per week
        # property.add_value('url', 'https://londonrelocation.com/properties-to-rent/properties/property-london/534465-2-bed-frognal-hampstead-nw3/')
        # return property.load_item()
