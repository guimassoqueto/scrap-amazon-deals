## Running the Bookscraper app

1. Create database
```bash
make db
```
2. Create database migrations
```bash
make migration
```
OR  
1. Create database and apply migrations
```bash
make db-migration
```

## Useful Commands

```bash
scrapy genspider bookspider books.toscrape.com
```
(write data into file)
```bash
scrapy crawl bookspider -O data.json (or data.csv)
```

(append data in a file)
```bash
scrapy crawl bookspider -o data.json (or data.csv)
```

(see FEEDS at settings.py)
(write the results in a file, specified in settings.py, without calling -O or -o)
```bash
scrapy crawl bookspider
```