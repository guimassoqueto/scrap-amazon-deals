import scrapy
from playwright_amazon.items import ProductItem
from playwright_amazon.helpers.get_category import get_category

from logging import getLogger

logger = getLogger("amazon_spyder.py")


class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon_spider"
    base_amazon_url = "https://www.amazon.com.br"

    def start_requests(self):
        # GET request
        yield scrapy.Request(
            "https://www.amazon.com.br/deals", meta={"playwright": True}
        )

    def parse(self, response):
        hrefs = response.css("a.a-link-normal::attr(href)").getall()[::2]
        for url in hrefs:
            if "/dp/" in url:
                yield response.follow(url, callback=self.parse_product_page)

            if "/deal" in url:
                yield response.follow(url, callback=self.parse_deals_page)

    def parse_product_page(self, response):
        product_item = ProductItem()
        product_item["title"] = response.css("title::text").get()
        product_item["id"] = response.url
        product_item["category"] = get_category(
            response.css("div#wayfinding-breadcrumbs_container").get()
        )
        product_item["reviews"] = (
            response.css("#acrCustomerReviewText::text").get() or "0"
        )
        yield product_item

    def parse_deals_page(self, response):
        hrefs = response.css("a.a-link-normal::attr(href)").getall()[::2]
        for url in hrefs:
            product_url = self.base_amazon_url + url
            yield response.follow(product_url, callback=self.parse_product_page)
