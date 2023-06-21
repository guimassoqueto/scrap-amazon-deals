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

env:
	cp .env.sample .env 