from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

count_of_units = 10
location = "москва"
query = "гостиница"
url = f'https://yandex.ru/maps/172/ufa/search/{location}%20{query}'
# url = 'https://yandex.ru/maps/172/ufa/search/%D0%B3%D0%BE%D1%81%D1%82%D0%B8%D0%BD%D0%B8%D1%86%D1%8B/?ll=55.978058%2C54.733242&sll=55.958727%2C54.735147&sspn=0.148659%2C0.145423&z=12'

#options
options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)  # без картинок
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled") #disable automation mode
#options.add_argument("--proxy-server=159.223.34.114:3128") #set proxy

s = Service(executable_path='/Users/aleksandrajmetov/PycharmProjects/pythonProject6/chromedriver/chromedriver')
driver = webdriver.Chrome(service=s, options=options)
driver.maximize_window()




def get_source_html(url=url):


    try:
        driver.get(url=url)
        wait = WebDriverWait(driver, 5)  #Время ожидания на поиск новых элементов на странице
        elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".search-snippet-view__link-overlay._focusable")))
        #собираем все динамически подгружаемые элементы и формируем список
        n = 0
        while len(elements) < count_of_units:
            time.sleep(1) #время ожидания перед прокруктой
            elements1 = len(elements)
            elements = driver.find_elements(By.CLASS_NAME, "search-business-snippet-view__content")
            driver.execute_script("arguments[0].scrollIntoView(true);", elements[-1])
            elements = driver.find_elements(By.CLASS_NAME, "search-business-snippet-view__content")
            elements2 = len(elements)
            if elements1 == elements2:
                n = n + 1
                if n >= 5:
                    break
            else:
                n = 0
        print('Собрано', len(elements)+1, 'элемента(ов)')
        wait = WebDriverWait(driver, 3)  # 3 секунд ожидания
        elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".search-snippet-view__link-overlay._focusable")))

        # собираем ссылки из списка собранных элементов
        href_list = []
        for i in elements:
            href_list.append(i.get_attribute('href'))

        #Собираем данные из найденных страниц и формируем словарь
        keys = {'href': [], 'name': [], 'adress': [], 'phone': [], 'rate': [], 'rate_count': [], 'site': [],
                'bill': []}
        for link in href_list:
            driver.get(link)
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            try:
                keys['href'].append(link)
            except:
                keys['href'].append('null')

            try:
                organization_name = soup.find("h1", {"class": "orgpage-header-view__header"}).text
                keys['name'].append(organization_name)

            except:
                keys['name'].append('null')
            try:
                organization_phone = soup.find("div", {"class": "orgpage-phones-view__phone-number"}).text
                keys['phone'].append(organization_phone.replace(" ", ""))

            except:
                keys['phone'].append('null')

            try:
                bill = soup.find('span', class_='business-features-view__valued-value')
                keys['bill'].append(bill.text)
            except:
                keys['bill'].append('null')

            try:
                site = soup.find('span', class_='business-urls-view__text')
                keys['site'].append(site.text)
            except:
                keys['site'].append('null')

            try:
                adress = soup.find('a', class_='orgpage-header-view__address')
                keys['adress'].append(adress.text)
            except:
                keys['adress'].append('null')

            try:
                rate = soup.find('span', class_='business-rating-badge-view__rating-text')
                keys['rate'].append(rate.text)
            except:
                keys['rate'].append('null')

            try:
                rate_count = soup.find('div', class_='business-header-rating-view__text _clickable')
                keys['rate_count'].append(rate_count.text)

            except:
                keys['rate_count'].append('null')

        # сохраняем собранный словарь в xlsx файл
        now = datetime.now()
        date_time_str = now.strftime("%Y-%m-%d_%H-%M-%S")  # сегодняшняя дата и время на имени Excel файла

        df = pd.DataFrame(keys)
        df.to_excel(f'{date_time_str}.xlsx')
        df
        print('Данные экспортированны в файл', date_time_str +'.xlsx')

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

def main():
    get_source_html()

if __name__ == '__main__':
    main()