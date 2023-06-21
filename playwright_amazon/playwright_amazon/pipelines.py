# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from playwright_amazon.helpers.postgres_helper import insert_into
from playwright_amazon.items import ProductFields
from re import search


class PlaywrightAmazonPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # strip all whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            adapter[field_name] = value.strip()

        # get product id
        value = adapter.get(ProductFields.ID.value)
        adapter[ProductFields.ID.value] = search(r"/dp/(\w{10})", value).groups()[0]

        # convert review count to integer
        value = adapter.get(ProductFields.REVIEWS.value)
        adapter[ProductFields.REVIEWS.value] = int(
            search(r"[\d\.]+", value).group().replace(".", "")
        )

        # convert rating to float and multiply by 2 to get an rating between 0 and 10
        value = adapter.get(ProductFields.RATING.value)
        adapter[ProductFields.RATING.value] = (
            float(value.split(" ")[0].replace(",", ".")) * 2
        )

        return item


class SaveToPostgresPipeline:
    async def process_item(self, item, spider):
        await insert_into("products", item)
        return item
