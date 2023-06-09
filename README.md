# scraper-scrapy
Scrapy is a scraper tool framework built in python


## Requirements
* [asdf](https://asdf-vm.com/)
* [Python Poetry Dependencies Manager](https://python-poetry.org/)
* Able to do `make` commands in the terminal
* [asdf python 3.11+](https://github.com/asdf-community/asdf-python)


## Init the project

1. init the virtual environment
```bash
make shell
```

2. install dependencies
```bash
make install
```

3. pre-commit hooks (to avoid bad commit messages, and do tests before commit)
```bash
make pre-commit
```


## Project Order
1. [bookscraper](./bookscraper/)


## Useful Commands
```bash
scrapy startproject <project-name>

(inside the project folder)
scrapy genspider bookspider <website-to-scrap>

(after code the spiders inside spiders/*spider.py)
scrapy crawl <spider-name> (name class attribute inside spiders/*spider.py)

scrapy crawl <spider-name> -O <filename>.<ext> (ext can be .json, .csv, etc.)
```