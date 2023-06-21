import scrapy


class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon_spider"

    def start_requests(self):
        # GET request
        yield scrapy.Request(
            "https://www.amazon.com.br/deals", meta={"playwright": True}
        )

    def parse(self, response):
        yield {"pages": response.css("li.a-disabled::text").getall()[-1]}
