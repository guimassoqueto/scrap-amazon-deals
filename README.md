# scrap-scrapy
Scrapy is a scraper tool framework built in python

### First Step
Certify that RabbitMq and Postgres are up and running. Use this repo to build the images (scrap folder):
[Containers](https://github.com/guimassoqueto/containers)

## Init the project

1. create .env file
```shell
make env
```
1. init the virtual environment
```shell
poetry shell
```

2. install dependencies
```shell
poetry install
```

3. pre-commit hooks (to avoid bad commit messages, and do tests before commit)
```shell
pre-commit install && pre-commit install --hook-type commit-msg
```

4. init the app
```shell
make a
```