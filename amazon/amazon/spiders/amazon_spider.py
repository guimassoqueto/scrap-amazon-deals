import scrapy
from amazon.items import ProductItem
from amazon.helpers.get_category import get_category
from amazon.helpers.get_generator import get_generator
from logging import getLogger

logger = getLogger("amazon_spyder.py")


class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon_spider"
    base_amazon_url = "https://www.amazon.com.br"

    def start_requests(self):
        # GET request

        for page in pages:
            yield scrapy.Request(page, meta={"playwright": True})

    def parse(self, response):
        hrefs = response.css("a.a-link-normal::attr(href)").getall()[::2]
        for url in hrefs:
            if "/dp/" in url:
                yield response.follow(url, callback=self.parse_product_page)

            elif "/deal" in url:
                yield response.follow(url, callback=self.parse_deals_page)

            else:
                continue

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
            if "/dp/" in url:
                product_url = self.base_amazon_url + "/dp/" + url.split("/dp/")[1]
                yield response.follow(product_url, callback=self.parse_product_page)

            else:
                continue
