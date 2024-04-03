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
            self.__get_images(items_info)
            self.__get_descriptions(items_info)
            self.__save_csv(items_info)
    
    def __create_csv(self):
        with open(f'wb_parse_{self.query}.csv', mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'бренд', 'id бренда', 'название', 'цена', 'бренд', 'рейтинг', 'количество оценок', 'айди поставщика', 'рейтинг поставщика', 'в наличии', 'ссылка на фото', 'описание'])

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
                                 product.volume,
                                 product.image_links,
                                 product.description
                                 ])

    @staticmethod
    def __get_basket_info(id:int):
        if  0 <= id <= 143:
                basket = "01"
        elif 144 <= id <= 287:
            basket = "02"
        elif 288 <= id <= 431:
            basket = "03"
        elif 432 <= id <= 719:
            basket = "04"
        elif 720 <= id <= 1007:
            basket = "05"
        elif 1008<= id <= 1061:
            basket = "06"
        elif 1062<= id <= 1115:
            basket = "07"
        elif 1116<= id <= 1169:
            basket = "08"
        elif 1170<= id <= 1313:
            basket = "09"
        elif 1314<= id <= 1601:
            basket = "10"
        elif 1602<= id <= 1655:
            basket = "11"
        elif 1656<= id <= 1919:
            basket = "12"
        elif 1920<= id <= 2045:
            basket = "13"
        elif 2046<= id <= 2189:
            basket = "14"
        elif 2091<= id <= 2405:
            basket = "15"
        else:
            basket = "16"
        return basket

    def __get_images(self, item_model: Items):
        for product in item_model.products:
            _vol = product.id//100000
            basket = self.__get_basket_info(_vol)
            
            # url = f'https://basket-{basket}.wbbasket.ru/vol{_vol}/part{product.id//1000}/{product.id}/images/big/1.jpg'
            # res = requests.get(url=url)
            # if res.status_code == 200:
                
            # for pics
            pic_link = ''.join([f'https://basket-{basket}.wbbasket.ru/vol{_vol}/part{product.id//1000}/{product.id}/images/big/{i}.jpg;' for i in range(1, product.pics+1)])
            product.image_links = pic_link 
            pic_link = ''
    
    def __get_descriptions(self, item_model: Items):
            # for descriptions
        for product in item_model.products:
            _vol = product.id//100000
            basket = self.__get_basket_info(_vol)

            desc_link = f'https://basket-{basket}.wbbasket.ru/vol{_vol}/part{product.id//1000}/{product.id}/info/ru/card.json'
            response = requests.get(desc_link).json()
            product.description = response['description']
            desc_link = ''

if __name__ == '__main__':
    p = Parser('https://www.wildberries.ru/catalog/pitanie/chay-kofe/chay')
    print(p.query)
    p.parse()