from scrapy.http.response.html import HtmlResponse
from re import search
from scrapy.selector.unified import Selector


def convert_price_to_number(price_string: str) -> float:
    price = search("[\d\,\.]+", price_string)
    return float(price.group().replace(".", "").replace(",", "."))


def loop_price_selectors(element: Selector):
    """
    Com o element selecionado e existente, roda um loop nos possíveis seletores
    que podem possuir o preço, e se esse seletor existir, retorna o conteúdo (innerText)
    do seletor.
    """
    possible_price_selectors = ["span.a-offscreen"]
    for selector in possible_price_selectors:
        has_content = element.css(f"{selector}::text").get()
        if has_content:
            return has_content
    return None


def get_price(response: HtmlResponse) -> str:
    price_container_element = response.css("#corePrice_feature_div")
    if price_container_element:
        price = loop_price_selectors(price_container_element[0])
        if price:
            return convert_price_to_number(price)
    del price_container_element

    # no caso de livros, #corePrice_feature_div existe, mas não contem dados relevantes, o elemento a ser capturado é outro
    book_price = response.css("#price::text").get()
    if book_price:
        return convert_price_to_number(book_price)
    del book_price

    # para ebooks kindle, o processo é semelhante ao de livros
    ebook_price = response.css("#kindle-price::text").get()
    if ebook_price:
        return convert_price_to_number(ebook_price)

    return 0.0
