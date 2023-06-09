import scrapy
from bookscraper.items import BookItem


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css("article.product_pod")
        for book in books:
            book_relative_url: str = book.css(
                "article.product_pod>div.image_container>a::attr(href)"
            ).get()

            if "catalogue/" in book_relative_url:
                book_url = "https://books.toscrape.com/" + book_relative_url
            else:
                book_url = "https://books.toscrape.com/catalogue/" + book_relative_url

            yield response.follow(book_url, callback=self.parse_book_page)

        next_page: str = response.css("li.next>a::attr(href)").get()
        if next_page is not None:
            if "catalogue/" in next_page:
                next_page_url = "https://books.toscrape.com/" + next_page
            else:
                next_page_url = "https://books.toscrape.com/catalogue/" + next_page
            yield response.follow(next_page_url, callback=self.parse)

    def parse_book_page(self, response):
        book_item = BookItem()
        book_container = response.css("div#content_inner")
        table_rows = book_container.css("table>tr")

        book_item["url"] = response.url
        book_item["title"] = book_container.css("h1::text").get()
        book_item["category"] = (
            response.css("ul.breadcrumb>li")[-2].css("a::text").get()
        )
        book_item["price"] = book_container.css(
            "div.col-sm-6.product_main>p.price_color::text"
        ).get()
        book_item["reviews"] = table_rows[-1].css("td::text").get()

        yield book_item
