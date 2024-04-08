from wb_parser import Parser 
from image_loader import get_images


def main(only_pics=False, only_tables=False):
    if only_pics and only_tables or only_pics and not only_tables:
        p = Parser('https://www.wildberries.ru/catalog/pitanie/chay-kofe/chay')
        p.parse()
        get_images('wb_parse_subject=406.csv', new_df=True)
    if only_pics and not only_tables:
        get_images('wb_parse_subject=406.csv', new_df=True)
    if only_tables and not only_pics:
        p = Parser('https://www.wildberries.ru/catalog/pitanie/chay-kofe/chay')
        p.parse()

if __name__ == "__main__":
    main()
