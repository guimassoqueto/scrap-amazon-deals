# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from enum import Enum
from scrapy.item import Item, Field


class ProductItem(Item):
    id = Field()
    title = Field()
    reviews = Field()
    rating = Field()


class ProductFields(Enum):
    ID = "id"
    TITLE = "title"
    REVIEWS = "reviews"
    RATING = "rating"
