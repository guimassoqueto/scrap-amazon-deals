from typing import Generator
import scrapy
from amazon.items import ProductItem
from amazon.helpers.get_category import get_category

from logging import getLogger

logger = getLogger("amazon_spyder.py")


def get_generator(
    deals_pages_count: int, invert: bool = False
) -> Generator[str, None, None]:
    first_page = "https://www.amazon.com.br/deals?deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%2522deals-collection-all-deals%2522%252C%2522sorting%2522%253A%2522FEATURED%2522%257D"
    url_format = lambda first_deals_page, current_page_number: first_deals_page.replace(
        "%253A0%", f"%253A{current_page_number * 3}0%"
    )
    if invert:
        return (
            url_format(first_page, i) for i in range(deals_pages_count * 2 - 1, -1, -1)
        )
    return (url_format(first_page, i) for i in range(0, deals_pages_count * 2 - 1))


class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon_spider"
    base_amazon_url = "https://www.amazon.com.br"

    def start_requests(self):
        # GET request

        pages = get_generator(34, invert=True)
        for page in pages:
            yield scrapy.Request(page, meta={"playwright": True})

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
