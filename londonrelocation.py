import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from property import Property


class LondonrelocationSpider(scrapy.Spider):
    name = 'londonrelocation'
    allowed_domains = ['londonrelocation.com']
    start_urls = ['https://londonrelocation.com/properties-to-rent/']
    page_num=2

    def parse(self, response):
        for start_url in self.start_urls:
            yield Request(url=start_url,
                          callback=self.parse_area)

    def parse_area(self, response):
        area_urls = response.xpath('.//div[contains(@class,"area-box-pdh")]//h4/a/@href').extract()
        for area_url in area_urls:
            LondonrelocationSpider.page_num=2
            yield Request(url=area_url,
                          callback=self.parse_area_pages)

    def parse_area_pages(self, response):
        all_items= response.css(".test-box")
        for i in all_items:
            property = ItemLoader(item=Property())
            property.add_value('title',i.css(".h4-space a::text").extract())
            property.add_value('price',i.css("h5::text").extract())
            property.add_value('url', i.css('.h4-space a::attr(href)').extract())
            
            yield property.load_item()
        next_page = str(response.request.url) + '&pageset='+str(LondonrelocationSpider.page_num)
        if LondonrelocationSpider.page_num < 3: 
            LondonrelocationSpider.page_num+=1
            yield Request(next_page, callback=self.parse_area_pages)