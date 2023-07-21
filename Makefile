COMPOSE=docker compose

#  init containers (postgres, migrate, rabbitmq) and start scraping
scrap:
	docker compose up -d && date +%s 1> /home/gmassoqueto/github-repos/scraper-beautiful-soup/timestamp && cd amazon && scrapy crawl amazon_spider -L ERROR

# open repository in browser
or:
	open https://github.com/guimassoqueto/scraper-scrapy

# create .env from .env.sample
env:
	cp .env.sample .env

rmq:
	docker compose up rabbitmq -d
