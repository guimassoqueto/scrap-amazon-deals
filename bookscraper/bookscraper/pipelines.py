# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from itemadapter import ItemAdapter
from bookscraper.items import BookField
from bookscraper.helpers.postgres_helper import insert_into


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # strip all whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            adapter[field_name] = value.strip()

        # category --> switch to lowercase
        value = adapter.get(BookField.CATEGORY.value)
        adapter[BookField.CATEGORY.value] = value.lower()

        # price --> convert to float
        value = adapter.get(BookField.PRICE.value)
        value = value.replace("£", "")
        adapter[BookField.PRICE.value] = float(value)

        # reviews --> convert string to number
        num_reviews_string = adapter.get(BookField.REVIEWS.value)
        adapter[BookField.REVIEWS.value] = int(num_reviews_string)

        return item


class SaveToPostgresPipeline:
    async def process_item(self, item, spider):
        await insert_into("books", item)
        return item
