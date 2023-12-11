import requests
from bs4 import BeautifulSoup as bs
from config import LINK


def parse_currencies():

    r = requests.get(LINK)
    soup = bs(r.text, 'html.parser')

    data_container = soup.find('div', class_='widget-currency_bank')
    table = data_container.find('table')

    currencies = {}

    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        val = row.find_all('th')
        currency = val[0].text.strip()
        buy = cells[0].find('span').text.strip()
        sale = cells[1].find('span').text.strip()
        currencies[currency] = {'buy': buy, 'sale': sale}

    return currencies


def parse_cash_market():

    r = requests.get(LINK)
    soup = bs(r.text, 'html.parser')

    data_container = soup.find('div', class_='widget-currency_cash')
    table = data_container.find('table')

    currencies = {}

    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        val = row.find_all('th')
        currency = val[0].text.strip()
        buy = cells[0].find('span').text.strip()
        sale = cells[1].find('span').text.strip()
        currencies[currency] = {'buy': buy, 'sale': sale}

    return currencies




