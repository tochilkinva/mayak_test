"""
Функция парсинга товаров по ссылке.
Передаем name, url, xpath и получаем dict[Название] = Цена: str
xpath в формате: '//*[@class="карточка товара"] | .//*[@class="название"] | .//*[@class="цена"]'

Для работы Selenium нужно скачать chromedriver.exe и кинуть в корень папки
https://chromedriver.chromium.org/downloads
"""
import os

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver


def init_browser() -> webdriver:
    """Настраиваем и возвращаем браузер"""
    dir_current = os.getcwd()
    driverLocation = dir_current + "\chromedriver.exe"
    chrome_options = Options()
    # chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--incognito")
    service = Service(executable_path=driverLocation)
    return webdriver.Chrome(service=service, options=chrome_options)


def get_goods(name: str, url: str, xpath: str) -> dict:
    """
    Получаем HTML одной страницы по url.
    Парсим результат по xpath: карточка товара - название - цена.
    Если name есть в названии, то добавляем в словарь.
    :return: dict['title']=price: str
    """
    browser = init_browser()
    try:
        browser.get(url)
        browser.implicitly_wait(0.5)
        xcard, xtitle, xprice = xpath.split(sep='|')

        cards = browser.find_elements(By.XPATH, xcard)
        goods = {}
        for card in cards:
            title = card.find_element(By.XPATH, xtitle).text
            if name.lower() in title.lower():
                price = card.find_element(By.XPATH, xprice).text
                price = ''.join([s for s in price if s.isdigit()])
                if not price:
                    price = 0
                goods[title] = price

        browser.quit()
        return goods

    except Exception as e:
        raise Exception(
            f'Не удалось получить данные: {e}')


if __name__ == "__main__":
    name = 'смартфон xiaomi 12 lite'
    url = 'https://mishka-shop.com/search/?q=%D1%81%D0%BC%D0%B0%D1%80%D1%82%D1%84%D0%BE%D0%BD+xiaomi+12+lite&send=Y&r=Y'
    xpath = '//*[@class="tabloid"] | .//*[@class="middle"] | .//*[@class="price"]'
    goods = get_goods(name, url, xpath)
    print('goods: ', goods)
    print('Done')
