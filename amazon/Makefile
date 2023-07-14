COMPOSE=docker compose

#  init containers (postgres, migrate, rabbitmq) and start scraping
scrap:
	docker compose up -d && scrapy crawl amazon_spider -L ERROR

# open repository in browser
or:
	open https://github.com/guimassoqueto/scraper-scrapy

# create .env from .env.sample
env:
	cp .env.sample .env 
