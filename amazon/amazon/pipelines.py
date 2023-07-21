# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from amazon.helpers.utils.regex_replacer import regex_replacer
from amazon.helpers.rabbitmq.publisher import RabbitMQPublisher
from amazon.helpers.database.postgres import PostgresDB
from amazon.helpers.spider_end.generate_pid_errors_file import (
    generate_pid_errors_file,
)
from amazon.items import ProductFields
from re import search, sub
from logging import getLogger
import os


logger = getLogger("pipelines.py")


class PlaywrightAmazonPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # strip all whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            if isinstance(value, str):
                adapter[field_name] = regex_replacer(value)

        # convert review count to integer
        value = adapter.get(ProductFields.REVIEWS.value)
        adapter[ProductFields.REVIEWS.value] = int(
            search(r"[\d\.]+", value).group().replace(".", "")
        )

        return item


class SaveToPostgresPipeline:
    async def process_item(self, item, spider):
        pg = PostgresDB()
        await pg.upsert_item("products", item)
        return item


class WritePidErrorsPipeline:
    def close_spider(self, spider):
        pid_errors_file = generate_pid_errors_file()
        pg = PostgresDB()
        non_inserted_pids = pg.select_non_inserted_ids(pid_errors_file)
        if non_inserted_pids:
            # TODO: enviar mensagens com os pids com problemas para a fila 'scrap-soup'
            publisher = RabbitMQPublisher()
            publisher.publish_failed_pids(non_inserted_pids)
            delete_files()
        else:
            logger.error("[SUCCESS]: The database is not missing any product")
            delete_files()


def delete_files() -> None:
    if (
        os.path.exists("pid_errors.log")
        or os.path.exists("logs.log")
        or os.path.exists("amazon_products.csv")
    ):
        os.remove("pid_errors.log")
        os.remove("logs.log")
        os.remove("amazon-products.csv")
