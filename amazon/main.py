from scrapy.cmdline import execute


def get_pages_to_scrap():
    valid_options = ("y", "n")
    user_input = input("[Y or N] You want to scrap all deals pages? ")
    user_input = user_input.lower()

    while user_input not in valid_options:
        user_input = input("[Y or N] You want to scrap all deals pages? ")

    if user_input == "n":
        user_input = input("How much pages? ")
        while not user_input.isdigit():
            user_input = input("How much pages? ")
        return f"pages={user_input}"
    else:
        return "pages=1000000"


if __name__ == "__main__":
    pages = get_pages_to_scrap()
    execute(["scrapy", "crawl", "amazon_spider", "-a", pages])
