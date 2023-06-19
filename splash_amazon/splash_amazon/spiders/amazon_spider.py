import scrapy
from scrapy_splash import SplashRequest


class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon_spider"
    allowed_domains = ["amazon.com.br"]
    start_urls = ["https://amazon.com.br"]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={"wait": 0.5})

    def parse(self, response):
        pass
