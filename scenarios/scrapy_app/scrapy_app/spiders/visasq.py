import scrapy


class VisasqSpider(scrapy.Spider):
    name = "visasq"
    allowed_domains = ["service.visasq.com"]
    start_urls = ["https://service.visasq.com"]

    def parse(self, response):
        pass
