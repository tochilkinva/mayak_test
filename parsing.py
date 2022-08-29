"""
Пока не доделано
"""
import os
import time

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import \
    expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.support.ui import \
    WebDriverWait  # available since 2.4.0


def init_browser():
    """Настраиваем и запускаем браузер"""
    # options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--ignore-ssl-errors')
    # return webdriver.Chrome(chrome_options=options)
    dir_current = os.getcwd()
    driverLocation = dir_current + "\chromedriver.exe"
    chrome_options = Options()
    chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')
    chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--incognito") 
    return Chrome(driverLocation, options=chrome_options)


def get_page(name, url, xpath):
    """Получаем HTML одной страницы с указанного url"""
    try:
        browser = init_browser()
        browser.get(url)
        # required_html = browser.page_source
        # print(required_html)
        time.sleep(10)
        # try:
        test = browser.find_elements(By.XPATH, xpath)
        for option in test:
            print("Value is: %s" % option.get_attribute('class'))
        print(test)
        # except Exception as e:
        #     print(e)



        browser.quit()
        return None # required_html

    except Exception as e:
        raise Exception(
            f'Не удалось получить данные: {e}')


def parsing_html(html:str):
    pass

def parsing_browser(browser, name, url, xpath):
    test = browser.find_elements(By.XPATH, xpath)
    print(test)

if __name__ == "__main__":
    name = 'смартфон xiaomi 12 lite'
    url = 'https://market.yandex.ru/catalog--mobilnye-telefony/34512430/list?srnum=1227&was_redir=1&rt=11&rs=eJwz6mdUSuaSv9h4Yc-FDRcbLjZdbLmw78JehYrMxPzcTAVDI4WczJJUgWOPHjIrsXAwCDAASU4Bfg2GLEJ6qtjNzQ0MLc2MGhgfn2INYKxi4QDSsxgJ6QMAu9w99w%2C%2C&text=%D1%81%D0%BC%D0%B0%D1%80%D1%82%D1%84%D0%BE%D0%BD%20xiaomi%2012%20lite&hid=91491&local-offers-first=0&glfilter=7893318%3A7701962'
    xpath = '//*/div'
    html = get_page(name, url, xpath)
    # parsing_html(html)

    print('Done')
