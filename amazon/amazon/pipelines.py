# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
from amazon.helpers.postgres_helper import upsert_query
from amazon.items import ProductFields
from re import search, sub
from amazon.settings import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_USER


class PlaywrightAmazonPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # strip all whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            adapter[field_name] = value.strip().replace("'", "")

        # remove ' | Amazon.com.br' from title
        value = adapter.get(ProductFields.TITLE.value)
        adapter[ProductFields.TITLE.value] = sub(
            r"[\||:]?\s*.mazon.com.br.?\s?", "", value
        )

        # get product id
        value = adapter.get(ProductFields.ID.value)
        adapter[ProductFields.ID.value] = search(r"/dp/(\w{10})", value).groups()[0]

        # convert review count to integer
        value = adapter.get(ProductFields.REVIEWS.value)
        adapter[ProductFields.REVIEWS.value] = int(
            search(r"[\d\.]+", value).group().replace(".", "")
        )

        return item


class SaveToPostgresPipeline:
    def __init__(self):
        ## Create/Connect to database
        self.connection = psycopg2.connect(
            host=POSTGRES_HOST,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            dbname=POSTGRES_DB,
        )

        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()

    def process_item(self, item, spider):
        ## Define insert statement
        self.cur.execute(upsert_query("products", item))

        ## Execute insert of data into database
        self.connection.commit()
        return item

    def close_spider(self, spider):
        ## Close cursor & connection to database
        self.cur.close()
        self.connection.close()
