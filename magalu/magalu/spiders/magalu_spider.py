import scrapy
from magalu.items import ProductItem
from urllib.parse import urljoin
from scrapy.http.response.html import HtmlResponse
import re

URLS = [
    "https://www.magazineluiza.com.br/beleza-e-perfumaria/l/pf/seller---magazineluiza/?page=1",
    "https://www.magazineluiza.com.br/beleza-e-perfumaria/l/pf/seller---magazineluiza/?page=2",
    "https://www.magazineluiza.com.br/beleza-e-perfumaria/l/pf/seller---magazineluiza/?page=3",
    "https://www.magazineluiza.com.br/beleza-e-perfumaria/l/pf/seller---magazineluiza/?page=4",
    "https://www.magazineluiza.com.br/beleza-e-perfumaria/l/pf/seller---magazineluiza/?page=5",
    "https://www.magazineluiza.com.br/beleza-e-perfumaria/l/pf/seller---magazineluiza/?page=6",
    "https://www.magazineluiza.com.br/beleza-e-perfumaria/l/pf/seller---magazineluiza/?page=7",
    "https://www.magazineluiza.com.br/beleza-e-perfumaria/l/pf/seller---magazineluiza/?page=8",
    "https://www.magazineluiza.com.br/beleza-e-perfumaria/l/pf/seller---magazineluiza/?page=9",
    "https://www.magazineluiza.com.br/beleza-e-perfumaria/l/pf/seller---magazineluiza/?page=10",
    "https://www.magazineluiza.com.br/beleza-e-perfumaria/l/pf/seller---epocacosmeticos-integra/?page=1",
    "https://www.magazineluiza.com.br/beleza-e-perfumaria/l/pf/seller---epocacosmeticos-integra/?page=2",
    "https://www.magazineluiza.com.br/beleza-e-perfumaria/l/pf/seller---epocacosmeticos-integra/?page=3",
    "https://www.magazineluiza.com.br/beleza-e-perfumaria/l/pf/seller---epocacosmeticos-integra/?page=4",
    "https://www.magazineluiza.com.br/beleza-e-perfumaria/l/pf/seller---epocacosmeticos-integra/?page=5",
    "https://www.magazineluiza.com.br/beleza-e-perfumaria/l/pf/seller---epocacosmeticos-integra/?page=6",
    "https://www.magazineluiza.com.br/beleza-e-perfumaria/l/pf/seller---epocacosmeticos-integra/?page=7",
    "https://www.magazineluiza.com.br/beleza-e-perfumaria/l/pf/seller---epocacosmeticos-integra/?page=8",
    "https://www.magazineluiza.com.br/beleza-e-perfumaria/l/pf/seller---epocacosmeticos-integra/?page=9",
    "https://www.magazineluiza.com.br/beleza-e-perfumaria/l/pf/seller---epocacosmeticos-integra/?page=10",
    "https://www.magazineluiza.com.br/cama-mesa-e-banho/l/cm/seller---magazineluiza/?page=1",
    "https://www.magazineluiza.com.br/cama-mesa-e-banho/l/cm/seller---magazineluiza/?page=2",
    "https://www.magazineluiza.com.br/cama-mesa-e-banho/l/cm/seller---magazineluiza/?page=3",
    "https://www.magazineluiza.com.br/eletrodomesticos/l/ed/seller---magazineluiza/?page=1",
    "https://www.magazineluiza.com.br/eletrodomesticos/l/ed/seller---magazineluiza/?page=2",
    "https://www.magazineluiza.com.br/eletrodomesticos/l/ed/seller---magazineluiza/?page=3",
    "https://www.magazineluiza.com.br/informatica/l/in/?page=1",
    "https://www.magazineluiza.com.br/casa-e-construcao/l/cj/seller---magazineluiza/?page=1",
    "https://www.magazineluiza.com.br/casa-e-construcao/l/cj/seller---magazineluiza/?page=2",
    "https://www.magazineluiza.com.br/casa-e-construcao/l/cj/seller---magazineluiza/?page=3",
    "https://www.magazineluiza.com.br/eletroportateis/l/ep/seller---magazineluiza/?page=1",
    "https://www.magazineluiza.com.br/eletroportateis/l/ep/seller---magazineluiza/?page=2",
    "https://www.magazineluiza.com.br/eletroportateis/l/ep/seller---magazineluiza/?page=3",
    "https://www.magazineluiza.com.br/games/l/ga/seller---magazineluiza/?page=1",
    "https://www.magazineluiza.com.br/mercado/l/me/seller---magazineluiza/?page=1",
    "https://www.magazineluiza.com.br/mercado/l/me/seller---magazineluiza/?page=2",
    "https://www.magazineluiza.com.br/mercado/l/me/seller---magazineluiza/?page=3",
    "https://www.magazineluiza.com.br/moveis/l/mo/seller---magazineluiza/?page=1",
    "https://www.magazineluiza.com.br/tv-e-video/l/et/seller---magazineluiza/?page=1",
    "https://www.magazineluiza.com.br/utilidades-domesticas/l/ud/seller---magazineluiza/?page=1",
    "https://www.magazineluiza.com.br/utilidades-domesticas/l/ud/seller---magazineluiza/?page=2",
    "https://www.magazineluiza.com.br/utilidades-domesticas/l/ud/seller---magazineluiza/?page=3",
]


class MagaluSpiderSpider(scrapy.Spider):
    name = "magalu_spider"
    base_url = "https://www.magazineluiza.com.br/"

    def start_requests(self):
        for url in URLS:
            yield scrapy.Request(url, meta={"playwright": True})

    def parse(self, response: HtmlResponse):
        hrefs = response.css(
            '[data-testid="product-card-container"]::attr(href)'
        ).getall()

        for href in hrefs:
            # product_url = urljoin(self.base_url, href)
            yield response.follow(href, callback=self.parse_product)

    def parse_product(self, response: HtmlResponse):
        product_item = ProductItem()
        product_item["category"] = get_category(response)
        product_item["id"] = response.url
        product_item["title"] = (
            response.css('[data-testid="heading-product-title"]::text')
            .get()
            .replace("'", "")
            .replace("\\", "")
        )
        product_item["reviews"] = get_reviews(response)
        product_item["free_shipping"] = "false"
        product_item["image_url"] = get_image(response)
        product_item["price"] = get_price(response)
        product_item["previous_price"] = (
            get_previous_price(response) or product_item["price"]
        )
        product_item["discount"] = round(
            (1 - (product_item["price"] / product_item["previous_price"])) * 100
        )

        yield product_item


def get_category(response: HtmlResponse) -> str:
    container = response.css('[data-testid="breadcrumb-container"]')
    container_items = container.css('[data-testid="breadcrumb-item"]')
    category = [
        item.css("::text").get()
        for item in container_items
        if item.css("::text").get() != None
    ][:-1]
    if category:
        return " ".join(category)
    return ""


def get_reviews(response: HtmlResponse) -> int:
    inner_text = response.css('[format="score-count"]::text').get()
    if inner_text:
        x = re.search(r"\((\d+)\)", inner_text)
        return int(x.group(1))
    return 0


def get_image(response: HtmlResponse) -> str:
    image_url = response.css(
        '[data-testid="image-selected-thumbnail"]::attr(src)'
    ).get()
    if image_url:
        return image_url
    return "https://raw.githubusercontent.com/guimassoqueto/mocks/main/images/404.webp"


def get_price(response: HtmlResponse) -> float:
    price_raw = response.css('[data-testid="price-value"]::text').get()
    price_value = re.search(r"[\d\.]+\,\d{2}$", price_raw).group()
    return float(price_value.replace(".", "").replace(",", "."))


def get_previous_price(response: HtmlResponse) -> float | None:
    price_raw = response.css('[data-testid="price-original"]::text').get()
    if price_raw:
        price_value = re.search(r"[\d\.]+\,\d{2}$", price_raw).group()
        return float(price_value.replace(".", "").replace(",", "."))
    return None
