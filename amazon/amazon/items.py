# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from enum import Enum
from scrapy.item import Item, Field


class ProductItem(Item):
    id = Field()
    title = Field()
    category = Field()
    reviews = Field()
    is_prime = Field()
    price = Field()
    discount = Field()


class ProductFields(Enum):
    ID = "id"
    TITLE = "title"
    CATEGORY = "category"
    REVIEWS = "reviews"
    IS_PRIME = "is_prime"
    PRICE = "price"
    DISCOUNT = "discount"
