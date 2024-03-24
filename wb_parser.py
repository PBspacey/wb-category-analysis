# id, название, цена, бренд, рейтинг, количество оценок, айди поставщика, рейтинг поставщика, картинка, описание
import requests 
import re
import csv
import json
import time
from models import Items


class Parser:
    def __init__(self, url:str):
        self.query = self.__dfs(self.__category_extracter(url))


    @staticmethod
    def __category_extracter(url:str):
        pattern = '(?<=catalog/).+?(?=\?|$)'
        category = re.search(pattern, url)[0]
        return category

    @staticmethod
    def __dfs(f):
        cat = f
        js = requests.get('https://static-basket-01.wbbasket.ru/vol0/data/main-menu-ru-ru-v2.json')
        els = js.json().copy()
        while els:
            node = els.pop()  
            if node.get('url', ' ') == '/catalog/' + cat:
                return node.get('query', '') 
            if 'childs' in node and node['childs']:
                els.extend(node['childs'])  
        return None

    def parse(self):
        page = 1
        self.__create_csv()
        while True:
            response = requests.get(
                f'https://catalog.wb.ru/catalog/product1/v2/catalog?appType=1&curr=rub&dest=-1257786&page={page}&{self.query}')

            print(response.status_code)
            if response.status_code == 429:
                time.sleep(10)
                continue
            else:
                page += 1
            items_info = Items.model_validate(response.json()['data'])
            if page % 10 == 0:
                print(page) 
            if not items_info.products:
                break
            self.__save_csv(items_info)
    
    def __create_csv(self):
        with open(f'wb_parse_{self.query}.csv', mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'бренд', 'id бренда', 'название', 'цена', 'бренд', 'рейтинг', 'количество оценок', 'айди поставщика', 'рейтинг поставщика', 'в наличии'])

    def __save_csv(self, items):
        with open(f'wb_parse_{self.query}.csv', mode='a', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            for product in items.products:
                writer.writerow([product.id,
                                 product.brand,
                                 product.brandId,
                                 product.name, 
                                 product.price, 
                                 product.brand,
                                 product.reviewRating,
                                 product.feedbacks,
                                 product.supplierId,
                                 product.supplierRating,
                                 product.volume
                                 ])


if __name__ == '__main__':
    p = Parser('https://www.wildberries.ru/catalog/pitanie/chay-kofe/chay')
    print(p.query)
    p.parse()