import scrapy

class JobItem(scrapy.Item):
    title = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    date_posted = scrapy.Field()
    salary = scrapy.Field()
    source = scrapy.Field()
