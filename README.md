# scraper-scrapy
Scrapy is a scraper tool framework built in python


## Requirements
* [asdf](https://asdf-vm.com/)
* [Python Poetry Dependencies Manager](https://python-poetry.org/)
* Able to do `make` commands in the terminal
* [asdf python 3.10+](https://github.com/asdf-community/asdf-python)


## Init the project

1. init the virtual environment
```bash
poetry shell
```

2. install dependencies
```bash
poetry install
```

3. pre-commit hooks (to avoid bad commit messages, and do tests before commit)
```bash
pre-commit install && pre-commit install --hook-type commit-msg
```

GREP ERRORS:
```bash
grep -oP '\[PRODUCT_ERROR\]:\s\w*' logs.log | awk -F" " '{ print $2 }' 1> pid_errors.log
```
