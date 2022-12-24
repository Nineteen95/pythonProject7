import pandas as pd
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import asyncio
import aiohttp
import requests

# Функция для получения списка прокси-серверов
def get_proxy_list():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    proxy_list = []
    for row in soup.find('table', attrs={'id': 'proxylisttable'}).find_all('tr')[1:]:
        proxy_list.append(row.find_all('td')[0].text + ':' + row.find_all('td')[1].text)
    return proxy_list

# Функция для получения цен товаров с aliexpress.com
async def get_aliexpress_prices(url, proxy_list):
    prices = []
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    for proxy in proxy_list:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, proxy=proxy, headers=headers) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        price = soup.find('span', attrs={'class': 'price-current'}).text
                        prices.append(price)
            except:
                pass
    return prices

# Функция для получения цен товаров с ozon.ru
async def get_ozon_prices(url, proxy_list):
    prices = []
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    for proxy in proxy_list:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, proxy=proxy, headers=headers) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        price = soup.find('span', attrs={'class': 'eOzonPrice_main'}).text
                        prices.append(price)
            except:
                pass
    return prices

# Функция для получения цен товаров с market.yandex.ru
async def get_yandex_prices(url, proxy_list):
    prices = []
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    for proxy in proxy_list:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, proxy=proxy, headers=headers) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        price = soup.find('span', attrs={'class': 'price_value'}).text
                        prices.append(price)
            except:
                pass
    return prices

# Функция для получения цен товаров с wildberries.com
async def get_wildberries_prices(url, proxy_list):
    prices = []
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    for proxy in proxy_list:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, proxy=proxy, headers=headers) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        price = soup.find('span', attrs={'class': 'price-value'}).text
                        prices.append(price)
            except:
                pass
    return prices

# Функция для получения цен товаров с различных сайтов
async def get_prices(urls):
    proxy_list = get_proxy_list()
    tasks = []
    for url in urls:
        if 'aliexpress' in url:
            task = asyncio.create_task(get_aliexpress_prices(url, proxy_list))
        elif 'ozon' in url:
            task = asyncio.create_task(get_ozon_prices(url, proxy_list))
        elif 'yandex' in url:
            task = asyncio.create_task(get_yandex_prices(url, proxy_list))
        elif 'wildberries' in url:
            task = asyncio.create_task(get_wildberries_prices(url, proxy_list))
        tasks.append(task)
    prices = await asyncio.gather(*tasks)
    return prices

# Функция для получения списка ссылок на товары с различных сайтов
def get_urls():
    chromedriver = "/Users/andreyinozemcev/Downloads/chromedriver"

    urls = []
    # Получение ссылок с aliexpress.com
    driver = webdriver.Chrome(chromedriver)
    driver.get('https://www.aliexpress.com/')
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a', attrs={'class': 'history-item product'}):
        urls.append(link.get('href'))
    driver.close()
    # Получение ссылок с ozon.ru
    driver = webdriver.Chrome(chromedriver)
    driver.get('https://www.ozon.ru/')
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a', attrs={'class': 'link'}):
        urls.append(link.get('href'))
    driver.close()
    # Получение ссылок с market.yandex.ru
    driver = webdriver.Chrome(chromedriver)
    driver.get('https://market.yandex.ru/')
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a', attrs={'class': 'link'}):
        urls.append(link.get('href'))
    driver.close()
    # Получение ссылок с wildberries.ru
    driver = webdriver.Chrome(chromedriver)
    driver.get('https://www.wildberries.ru/')
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a', attrs={'class': 'ref_goods_n_p'}):
        urls.append(link.get('href'))
    driver.close()
    return urls

# Основная функция
def main():
    urls = get_urls()
    prices = asyncio.run(get_prices(urls))
    df = pd.DataFrame(prices, columns=['Price'])
    df.to_csv('prices.csv', index=False)

if __name__ == '__main__':
    main()

