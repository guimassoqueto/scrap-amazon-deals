COMPOSE=docker compose

# init virtual env
s:
	poetry shell

# install dependencies
i:
	poetry install

pc:
	pre-commit install && pre-commit install --hook-type commit-msg

# open repository in browser
or:
	open https://github.com/guimassoqueto/scraper-scrapy

# run tests
t: 
	pytest