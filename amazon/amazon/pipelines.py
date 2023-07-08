# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from typing import List, Tuple
from itemadapter import ItemAdapter
from amazon.helpers.postgres_service import PostgresDB
from amazon.helpers.generate_pid_errors_file import generate_pid_errors_file
from amazon.items import ProductFields
from re import search, sub
from logging import getLogger
from amazon.settings import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)

logger = getLogger("pipelines.py")


class PlaywrightAmazonPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # strip all whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            if isinstance(value, str):
                adapter[field_name] = sub(r"[^a-zA-Zà-úÀ-Ú0-9_\s\.>]", "", value)

        # convert review count to integer
        value = adapter.get(ProductFields.REVIEWS.value)
        adapter[ProductFields.REVIEWS.value] = int(
            search(r"[\d\.]+", value).group().replace(".", "")
        )

        return item


class SaveToPostgresPipeline:
    async def process_item(self, item, spider):
        pg = PostgresDB(
            POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT
        )
        await pg.upsert_item("products", item)
        return item


class WritePidErrorsPipeline:
    def close_spider(self, spider):
        pid_errors_file = generate_pid_errors_file("logs.log")
        pg = PostgresDB(
            POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT
        )
        non_inserted_ids = pg.select_non_inserted_ids(pid_errors_file)
        if non_inserted_ids:
            self.write_non_inserted_ids_file(non_inserted_ids)
        else:
            logger.error("[SUCCESS]: The database is not missing any product")

    def write_non_inserted_ids_file(
        self,
        non_inserted_ids: List[Tuple[str]],
        output_file: str = "/home/gmassoqueto/github-repos/scraper-beautiful-soup/insertion_errors.log",
    ) -> None:
        with open(output_file, "w", encoding="utf-8") as f:
            for non_inserted_id in non_inserted_ids:
                f.write(f"{non_inserted_id[0]}\n")
