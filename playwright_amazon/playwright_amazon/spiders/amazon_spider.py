import scrapy
from playwright_amazon.items import ProductItem
from playwright_amazon.helpers.get_category import get_category


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
        product_item["title"] = response.css("span#productTitle::text").get()
        product_item["id"] = response.url

        container = response.css("span.cr-widget-TitleRatingsHistogram")
        product_item["reviews"] = container.css(
            "span.a-size-base.a-color-secondary::text"
        ).get()
        product_item["rating"] = container.css(
            "span.a-size-medium.a-color-base::text"
        ).get()

        product_item["category"] = get_category(
            response.css("div#wayfinding-breadcrumbs_feature_div").get()
        )

        yield product_item

    def parse_deals_page(self, response):
        hrefs = response.css("a.a-link-normal::attr(href)").getall()[::2]
        for url in hrefs:
            product_url = self.base_amazon_url + url
            yield response.follow(product_url, callback=self.parse_product_page)
