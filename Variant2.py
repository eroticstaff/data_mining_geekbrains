import requests
from bs4 import BeautifulSoup as bs
import json
from pprint import pprint


def getCategories(content):
    soup = bs(content, 'html.parser')
    products_categories_soup = soup.find('div', attrs={'class': 'testlab-category'})
    products_categories = []
    if products_categories_soup != None:
        for item in products_categories_soup.find_all('a', attrs={'class': 'catalog__category-item'}):
            category_name = item.find('div', attrs={'class': 'catalog__category-name'}).getText()
            category_url = url + item['href']
            category = {
                'category_name': category_name.lstrip(),
                'category_url': category_url
            }
            products_categories.append(category)
    else:
        return False
    return products_categories


def getProducts(content):
    soup = bs(content, 'html.parser')
    products_soup = soup.find_all('a', attrs={'class': 'block-product-catalog__item'})
    products = []
    for product in products_soup:
        product_name = product.find('div', attrs={'class': 'product__item-link'}).getText()
        product_url = product['href']
        rating = {}
        if len(list(product.find_all('div', attrs={'class': 'rate blacklist-value'}))) == 0:
            rating_block = product.find('div', attrs={'class': 'rating-block'})
            if rating_block != None:
                rating_block_children = rating_block.findChildren(recursive=False)
                if len(rating_block_children) == 4:
                    for row in rating_block_children:
                        row_children = row.findChildren(recursive=False)
                        rating_name = row_children[0].find('div', attrs={'class': 'text'}).getText()
                        rating_number = int(row_children[1].getText())
                        rating[rating_name] = rating_number
        else:
            rating = "В черном списке"
        product_data = {
            'product_name': product_name,
            'product_url': product_url,
            'rating': rating
        }
        products.append(product_data)
    return products


url = 'https://roscontrol.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}
response = requests.get(url + '/category/produkti/', headers=headers)
products_categories = getCategories(response.text)
print(products_categories)
print("Добро пожаловать в парсер сайта Россконтроля!")
print("Выберите категорию продуктов:")
for i, category in enumerate(products_categories):
    print(str(i + 1) + ":", category['category_name'])
category_num = int(input(">> ")) - 1
print("Вы выбрали", products_categories[category_num]['category_name'])
response = requests.get(products_categories[category_num]['category_url'], headers=headers)
products_subcategories = getCategories(response.text)
if products_subcategories:
    print("Выберите подкатегорию продуктов:")
    for i, category in enumerate(products_subcategories):
        print(str(i + 1) + ":", category['category_name'])
    subcategory_num = int(input(">> ")) - 1
    print("Вы выбрали", products_subcategories[subcategory_num]['category_name'])
    response = requests.get(products_subcategories[subcategory_num]['category_url'], headers=headers)
    print("Список продуктов:")
    products = getProducts(response.text)
    for product in products:
        print(product['product_name'])
        if type(product['rating']) != str:
            for key in product['rating']:
                print('\t' + key + ":" + str(product['rating'][key]))
        else:
            print('\t' + product['rating'])
    with open("products.json", 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False)
else:
    print("Список продуктов:")
    products = getProducts(response.text)
    for product in products:
        print(product['product_name'])
        if type(product['rating']) != str:
            for key in product['rating']:
                print('\t'+key+":"+str(product['rating'][key]))
        else:
            print('\t'+product['rating'])
    with open("products.json", 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False)