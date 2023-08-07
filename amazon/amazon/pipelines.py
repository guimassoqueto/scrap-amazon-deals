# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from logging import getLogger
import os
from csv import DictReader

from amazon.infra.rabbitmq.publisher import RabbitMQPublisher


logger = getLogger("pipelines.py")


class PlaywrightAmazonPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        return item


class SendMessagePipeline:
    def close_spider(self, spider):
        pids = get_pids("amazon-products.csv")
        publisher = RabbitMQPublisher()
        publisher.publish_pids(pids)
        delete_files()


def get_pids(csv_file: str) -> dict:
    pids = set()
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = DictReader(f)
        for row in reader:
            pids.add(row["id"])
    return {
        "amazon-colly": list(pids)
    }  # TODO: usar pydantic para definir o formato do objeto


def delete_files() -> None:
    if os.path.exists("logs.log") or os.path.exists("amazon_products.csv"):
        os.remove("logs.log")
        os.remove("amazon-products.csv")
