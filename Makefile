COMPOSE=docker compose

#  init containers (postgres, migrate, rabbitmq) and start scraping
a:
	 cd amazon && scrapy crawl amazon_spider -L INFO

# open repository in browser
or:
	open https://github.com/guimassoqueto/scraper-scrapy

# create .env from .env.sample
env:
	cp .env.sample .env

rmq:
	docker compose up rabbitmq -d
