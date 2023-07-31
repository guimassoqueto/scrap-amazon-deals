COMPOSE=docker compose

#  init containers (postgres, migrate, rabbitmq) and start scraping
a:
	cd amazon && poetry run python main.py

# open repository in browser
or:
	open https://github.com/guimassoqueto/scraper-scrapy

# create .env from .env.sample
env:
	cp .env.sample .env

req:
	poetry export -f requirements.txt --output requirements.txt

