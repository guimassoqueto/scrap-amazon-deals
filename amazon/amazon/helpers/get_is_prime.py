from scrapy.http.response.html import HtmlResponse


def get_is_prime(response: HtmlResponse) -> str:
    prime_div = response.css("#primeSavingsUpsellCaption_feature_div").get()
    if prime_div is not None:
        return "true"

    prime_div = response.css(
        "div.tabular-buybox-text:nth-child(4)>div:nth-child(1)>span:nth-child(1)::text"
    ).get()
    if prime_div is not None and "amazon" in prime_div.strip().lower():
        return "true"

    prime_div = (
        response.css(
            "#mir-layout-DELIVERY_BLOCK-slot-PRIMARY_DELIVERY_MESSAGE_LARGE>span::text"
        )
        .get()
        .strip()
        .lower()
    )
    if prime_div is not None and "grátis" in prime_div:
        return "true"

    return "false"
