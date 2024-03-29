from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def get_total_deals_pages() -> int:
    try:
        options = Options()
        options.add_argument("--headless=new")
        options.page_load_strategy = "eager"
        driver = webdriver.Chrome(options=options)
        driver.get("http://www.amazon.com.br/deals")
        element = driver.find_element(
            by=By.CSS_SELECTOR, value="ul.a-pagination>li:nth-last-child(2)"
        )
        total = int(element.text)
        driver.quit()
        return total
    except Exception as e:
        return 1
