import scrapy
from amazon.items import ProductItem
from amazon.helpers.get_category import get_category
from amazon.helpers.get_generator import get_generator
from logging import getLogger

logger = getLogger("amazon_spyder.py")


class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon_spider"
    base_amazon_url = "https://www.amazon.com.br"
    current_offers_page = 1
    total_offer_pages = 33  # adicionar metodo para descobrir numero de paginas em promo

    def start_requests(self):
        # GET request
        scrap_all_deals = False

        if scrap_all_deals:
            pages = get_generator(self.total_offer_pages)
            for page in pages:
                logger.error(
                    f"[START REQUESTS] Scraping all deals pages {self.current_offers_page} of {self.total_offer_pages}"
                )
                yield scrapy.Request(page, meta={"playwright": True})
                self.current_offers_page += 1
        else:
            logger.error(
                f"[START REQUESTS] Scraping only the first deals page {self.current_offers_page} of {self.total_offer_pages}"
            )
            yield scrapy.Request(
                "https://www.amazon.com.br/deals",
                dont_filter=True,
                meta={"playwright": True},
            )

    def parse(self, response):
        response_url = response.url
        if "/dp/" not in response_url:
            logger.error("NOT /DP/")
            hrefs = response.css("a.a-link-normal::attr(href)").getall()[::2]

            for url in hrefs:
                if "/dp/" in url:
                    yield response.follow(url, callback=self.parse_product_page)

                elif "/deal/" in url:
                    yield response.follow(url, callback=self.parse_deals_page)
        else:
            yield response.follow(response_url, callback=self.parse_product_page)

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

        product_title = str(product_item["title"]).strip().lower()
        if (
            product_title == "amazon.com.br"
            or product_title == ""
            or product_title is None
        ):
            logger.error(f'[PRODUCT ERROR]: {product_item["id"]}')
            yield response.follow(response.url, callback=self.parse_product_page)
        else:
            yield product_item

    def parse_deals_page(self, response):
        hrefs = response.css("a.a-link-normal::attr(href)").getall()[::2]

        for url in hrefs:
            product_url = self.base_amazon_url + url
            yield response.follow(product_url, callback=self.parse_product_page)
