import scrapy
from amazon.items import ProductItem
from logging import getLogger
from re import search
from amazon.helpers.selenium.get_total_deals_pages import get_total_deals_pages
from amazon.helpers.spider_start.get_deals_pages_generator import (
    get_deals_pages_generator,
)

logger = getLogger("amazon_spyder.py")

deals_patterns = [
    "/gp/goldbox",
    "deals-widget=",
    "deals?",
    "/deal/",
    "showVariations=true",
    "hidden-keywords=",
    "s?k=",
]


class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon_spider"
    base_amazon_url = "https://www.amazon.com.br/"
    current_offers_page = 1
    total_offer_pages = get_total_deals_pages()

    def start_requests(self):
        pages = get_deals_pages_generator(self.total_offer_pages)

        for page in pages:
            logger.info(
                f"[START_REQUESTS] Scraping all deals pages {self.current_offers_page / 2} of {self.total_offer_pages}"
            )
            yield scrapy.Request(page, meta={"playwright": True})
            self.current_offers_page += 1

    def parse(self, response):
        if "/dp/" in response.url:
            product_item = ProductItem()
            product_item["id"] = search(r"/dp/([A-Z0-9]+)", response.url).groups()[0]
            yield product_item

        else:
            hrefs = response.css("a.a-link-normal::attr(href)").getall()
            for href in hrefs:
                if "/dp/" in href:
                    product_item = ProductItem()
                    product_item["id"] = search(r"/dp/([A-Z0-9]+)", href).groups()[0]
                    yield product_item
                else:
                    for pattern in deals_patterns:
                        if pattern in href:
                            yield response.follow(href, callback=self.parse_deals)

    def parse_deals(self, response):
        hrefs = response.css("a.a-link-normal::attr(href)").getall()
        for url in hrefs:
            if "/dp/" in url:
                product_item = ProductItem()
                try:
                    product_item["id"] = search(r"/dp/([A-Z0-9]+)", url).groups()[0]
                    yield product_item
                except Exception as e:
                    product_item["id"] = search(r"_([A-Z0-9]{10})_", url).groups()[0]
                    yield product_item

            elif any(pattern in deals_patterns for pattern in url):
                yield response.follow(url, callback=self.parse_deals)
