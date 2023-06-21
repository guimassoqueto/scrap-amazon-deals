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
2. [splash amazon - dont work](./splash_amazon/)
3. [plawywight amazon - working](./playwright_amazon/)
