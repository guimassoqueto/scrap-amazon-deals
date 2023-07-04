COMPOSE=docker compose

db:
	${COMPOSE} up postgres -d

migrate:
	${COMPOSE} up migrate

db-migrate:
	${COMPOSE} up postgres migrate -d

# open repository in browser
or:
	open https://github.com/guimassoqueto/scraper-scrapy

# create .env from .env.sample
env:
	cp .env.sample .env 

scrap:
	make db-migrate && rm *.csv && rm *.log&& scrapy crawl amazon_spider -L ERROR
