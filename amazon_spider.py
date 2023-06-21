import scrapy


class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon_spider"
    allowed_domains = ["amazon.com.br"]
    start_urls = ["https://amazon.com.br"]

    def parse(self, response):
        pass
