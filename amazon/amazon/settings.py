# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
# https://docs.scrapy.org/en/latest/topics/settings.html
# https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html


from dotenv import load_dotenv
from os import getenv
from scrapy.utils.log import configure_logging
from logging import basicConfig, INFO

# configure logging
configure_logging(install_root_handler=False)
basicConfig(
    filename="logs.log",
    format="[%(asctime)s] %(name)s %(levelname)s: %(message)s",
    level=INFO,
)
# end logging

load_dotenv()

# start .env variables
POSTGRES_PORT = getenv("POSTGRES_PORT") or 5432
POSTGRES_DB = getenv("POSTGRES_DB") or "postgres"
POSTGRES_USER = getenv("POSTGRES_USER") or "postgres"
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD") or "password"
POSTGRES_HOST = getenv("POSTGRES_HOST") or "127.0.0.1"
# end .env variables


BOT_NAME = "amazon"
SPIDER_MODULES = ["amazon.spiders"]
NEWSPIDER_MODULE = "amazon.spiders"


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "amazon.middlewares.FakeHeaderMiddleware": 400,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "amazon.pipelines.PlaywrightAmazonPipeline": 300,
    "amazon.pipelines.SaveToPostgresPipeline": 400,
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

PLAYWRIGHT_BROWSER_TYPE = "firefox"

PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,
    "timeout": 20 * 1000,  # 20 seconds
}

FEEDS = {"amazon-products.csv": {"format": "csv"}}
