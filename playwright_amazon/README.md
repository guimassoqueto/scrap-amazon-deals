## Init

0. Run:
```shell
poetry shell
```

1. Run:
```shell
poetry install
```

2. At root directory
```shell
cd playwright_amazon
```

3. Run:
```shell
make env
```

4. Run:
```shell
make db-migrate
```

5. Run:
```shell
scrapy crawl amazon_spider -O data.csv
```