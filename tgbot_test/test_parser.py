import requests
from requests import Response
from requests.exceptions import HTTPError 
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: float


@dataclass
class Shop:
    name: str 
    products: list[Product]


def get_all_dicounts() -> list[Shop]:
    all_actions = []
    shops_name = ['Санта','Виталюр','Соседи']
    actions = [_get_santa_discounts(), 
              _get_vitalur_discounts(), 
              _get_sosedi_discounts()]
    for shop, action in zip(shops_name, actions):
        all_actions.append(Shop(
            name=shop,
            products=action)
        )
    return all_actions
    



def _get_response(url: str) -> Response: 
    ua = UserAgent()
    headers = {'user-agent': f'{ua.random}'}
    try:
        response = requests.get(
                url=url,
                headers=headers
                )
        response.raise_for_status()
        
    except HTTPError:
        raise HTTPError

    else: return response
    

def _get_santa_discounts() -> list[Product]:
    page = 1
    first_page = ' '
    products = []
    while True:
        url = f'https://santa.by/pokupatelyam/vygodnye-predlozheniya/goods/ay-da-tsena/?DISCOUNT=ay-da-tsena&PAGEN_1={page}'
        r = _get_response(url)
        soup = bs(r.text, "html.parser")
        all_products = soup.find_all('p', class_ ='card__text')
        all_prices = soup.find_all('span', class_ = 'price__num')


        if page == 1:
            first_page = all_products
        if first_page == all_products and page != 1:

            return products 

        for name_html, price_html in zip(all_products, all_prices):
            name = name_html.text
            price = float(price_html.text[:-2] + '.' + price_html.text[-2:])  
            products.append(Product(
                name = name,
                price = price,
            ))            
        page += 1


def _get_vitalur_discounts() -> list[Product]:
    page = 1
    first_page = ' '
    products = []
    while True:
        url = f"https://vitalur.by/actions/?PAGEN_1={page}&action_section=0&products_section="
        r = _get_response(url)
        soup = bs(r.text, "html.parser")
        all_products = soup.find_all('div', class_ ='card-bottom')
        
        if page == 1:
            first_page = all_products
        if first_page == all_products and page != 1:
            return products

        for info in products:
            info = info.text
            info_list = info.split('\n')
            info_list = list(filter(None, info_list))
            name = info_list[0]
            new_price = info_list[1] + '.' + info_list[2]
            products.append(Product(
                name = name,
                price = new_price,
            )) 
        page += 1


def _get_sosedi_discounts() -> list[Product]:
    page = 1
    ua = UserAgent()
    products = []

    while True:
        url = 'https://sosedi.by/local/api/getListProducts.php'
        data = {'paginationItem': page,
                'selected': "all",
                'selectedCategory': "all"}
        headers = {'user-agent': f'{ua.random}'} 

        resp = requests.post(url, headers=headers, json=data)
        resp = resp.json()
        items = resp.get('items')
        if len(items) == 0:
            return products
        for item in items:
            name = item[0]['title']
            price = item[0]['price']
            products.append(Product(
                name=name,
                price=price,
            ))
        page += 1




