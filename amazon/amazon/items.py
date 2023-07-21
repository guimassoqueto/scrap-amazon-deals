# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from enum import Enum
from scrapy.item import Item, Field


class ProductItem(Item):
    id = Field()
    title = Field()
    image_url = Field()
    category = Field()
    reviews = Field()
    free_shipping = Field()
    price = Field()
    previous_price = Field()
    discount = Field()


class ProductFields(Enum):
    ID = "id"
    TITLE = "title"
    IMAGE_URL = "image_url"
    CATEGORY = "category"
    REVIEWS = "reviews"
    FREE_SHIPPING = "free_shipping"
    PRICE = "price"
    PREVIOUS_PRICE = "previous_price"
    DISCOUNT = "discount"
