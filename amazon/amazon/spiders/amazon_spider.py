import scrapy
from amazon.items import ProductItem
from amazon.helpers.get_category import get_category
from amazon.helpers.get_generator import get_generator
from amazon.helpers.get_is_prime import get_is_prime
from logging import getLogger


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
    total_offer_pages = 45  # adicionar metodo para descobrir numero de paginas em promo

    def start_requests(self):
        scrap_all_deals = True

        if scrap_all_deals:
            pages = get_generator(self.total_offer_pages)
            for page in pages:
                logger.error(
                    f"[START REQUESTS] Scraping all deals pages {self.current_offers_page / 2} of {self.total_offer_pages}"
                )
                yield scrapy.Request(page, meta={"playwright": True})
                self.current_offers_page += 1
        else:
            page = "https://www.amazon.com.br/deals"
            logger.error(f"[START REQUESTS] Scraping page: {page}")
            yield scrapy.Request(
                page,
                dont_filter=True,
                meta={"playwright": True},
            )

    def parse(self, response):
        if "/dp/" in response.url:
            yield response.follow(response.url, callback=self.parse_product)

        else:
            hrefs = response.css("a.a-link-normal::attr(href)").getall()
            for href in hrefs:
                if self.base_amazon_url in href:
                    if "/dp/" in href:
                        yield response.follow(href, callback=self.parse_product)
                    else:
                        for pattern in deals_patterns:
                            if pattern in href:
                                yield response.follow(href, callback=self.parse_deals)
                else:
                    logger("[HREF ERROR]", href)

    def parse_product(self, response):
        product_item = ProductItem()
        product_item["title"] = response.css("title::text").get()
        product_item["id"] = response.url
        product_item["category"] = get_category(
            response.css("div#wayfinding-breadcrumbs_container").get()
        )
        product_item["reviews"] = (
            response.css("#acrCustomerReviewText::text").get() or "0"
        )
        product_item["is_prime"] = get_is_prime(response)

        product_title = str(product_item["title"]).strip().lower()
        if (
            product_title == "amazon.com.br"
            or product_title == ""
            or product_title is None
        ):
            pid = product_item["id"].split("/dp/")[1][10]
            logger.error(f"[PRODUCT ERROR]: {pid}")
            yield response.follow(response.url, callback=self.parse_product)
        else:
            yield product_item

    def parse_deals(self, response):
        hrefs = response.css("a.a-link-normal::attr(href)").getall()
        for url in hrefs:
            if "/dp/" in url:
                yield response.follow(url, callback=self.parse_product)

            elif any(pattern in deals_patterns for pattern in url):
                yield response.follow(url, callback=self.parse_deals)
