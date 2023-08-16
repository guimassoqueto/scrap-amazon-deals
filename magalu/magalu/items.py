# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ProductItem(Item):
    id = Field()
    title = Field()
    category = Field()
    reviews = Field()
    free_shipping = Field()
    image_url = Field()
    price = Field()
    previous_price = Field()
    discount = Field()
