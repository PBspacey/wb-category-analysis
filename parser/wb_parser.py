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
            self.__save_csv(items_info)
    
    def __create_csv(self):
        with open(f'wb_parse_{self.query}.csv', mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'бренд', 'id бренда', 'название', 'цена', 'бренд', 'рейтинг', 'количество оценок', 'айди поставщика', 'рейтинг поставщика', 'в наличии', 'ссылка на фото'])

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
                                 product.image_links
                                 ])

    def __get_images(self, item_model: Items):
        for product in item_model.products:
            _vol = product.id//100000
            if  0 <= _vol <= 143:
                basket = "01"
            elif 144 <= _vol <= 287:
                basket = "02"
            elif 288 <= _vol <= 431:
                basket = "03"
            elif 432 <= _vol <= 719:
                basket = "04"
            elif 720 <= _vol <= 1007:
                basket = "05"
            elif 1008<= _vol <= 1061:
                basket = "06"
            elif 1062<= _vol <= 1115:
                basket = "07"
            elif 1116<= _vol <= 1169:
                basket = "08"
            elif 1170<= _vol <= 1313:
                basket = "09"
            elif 1314<= _vol <= 1601:
                basket = "10"
            elif 1602<= _vol <= 1655:
                basket = "11"
            elif 1656<= _vol <= 1919:
                basket = "12"
            elif 1920<= _vol <= 2045:
                basket = "13"
            elif 2046<= _vol <= 2189:
                basket = "14"
            elif 2091<= _vol <= 2405:
                basket = "15"
            else:
                basket = "16"
            url = f'https://basket-{basket}.wbbasket.ru/vol{_vol}/part{product.id//1000}/{product.id}/images/big/1.jpg'
            # res = requests.get(url=url)
            # if res.status_code == 200:
            link_str = ''.join([f'https://basket-{basket}.wbbasket.ru/vol{_vol}/part{product.id//1000}/{product.id}/images/big/{i}.jpg;' for i in range(1, product.pics+1)])
            product.image_links = link_str 
            link_str = ''


if __name__ == '__main__':
    p = Parser('https://www.wildberries.ru/catalog/pitanie/chay-kofe/chay')
    print(p.query)
    p.parse()