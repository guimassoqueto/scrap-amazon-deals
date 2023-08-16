# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from itemadapter import ItemAdapter

from magalu.helpers.postgres.postgres import PostgresDB


class PlaywrightMagaluPipeline:
    async def process_item(self, item, spider):
        await PostgresDB.upsert_item("items", ItemAdapter(item).asdict())
        return item


class FinishSpiderPipeline:
    def close_spider(self, spider):
        delete_files()


def delete_files() -> None:
    if os.path.exists("logs.log") or os.path.exists("magalu-products.csv"):
        os.remove("logs.log")
        os.remove("magalu-products.csv")
