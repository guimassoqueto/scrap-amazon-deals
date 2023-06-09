# init virtual env
shell:
	poetry shell

# install dependencies
install:
	poetry install

pre-commit:
	pre-commit install && pre-commit install --hook-type commit-msg

# open repository in browser
or:
	open https://github.com/guimassoqueto/scraper-scrapy

# run tests
t: 
	pytest