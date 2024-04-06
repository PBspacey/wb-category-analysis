from wb_parser import Parser 
from image_loader import get_images


if __name__ == "__main__":
    p = Parser('https://www.wildberries.ru/catalog/pitanie/chay-kofe/chay')
    p.parse()
    get_images('wb_parse_subject=406.csv')
