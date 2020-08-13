import json
import requests
from datetime import date
import pandas as pd
import os


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'Accept': 'application/json'
}
# 4. Creggs
path_greggs = './greggs_' + date.today().strftime("%b-%d-%Y")
os.mkdir(path_greggs)

start_urls = [
    'https://api.greggs.co.uk/1.0/product/category/breakfast?banner_width=640&product_width=200',
    'https://api.greggs.co.uk/1.0/product/category/drinks-and-snacks?banner_width=640&product_width=200',
    'https://api.greggs.co.uk/1.0/product/category/sandwiches?banner_width=640&product_width=200'
    ' https://api.greggs.co.uk/1.0/product/category/bakes?banner_width=640&product_width=200',
    'https://api.greggs.co.uk/1.0/product/category/sweet-treats?banner_width=640&product_width=200',
    'https://api.greggs.co.uk/1.0/product/category/balanced-choice?banner_width=640&product_width=200'
]

greggs = []
for category in start_urls:
    product_list = requests.get(category, headers=headers).json().get('products')
    for product in product_list:
        product_slug = product['product_slug']
        product_url = f'https://api.greggs.co.uk/1.0/product/slug/{product_slug}?banner_width=400&product_width=400'
        product = requests.get(product_url, headers=headers).json()
        item_id = product['id']
        fileName = path_greggs + '/item_' + item_id + '_' + product_slug + '.json'
        with open(fileName, 'w') as f:
            json.dump(product, f)
        product_dict = {'Product_id': item_id, 'Product_Name': product['name'],
                        'Product_Title': product['meta_title'], 'Product_Description': product['meta_description'],
                        'Product_Allergens': product['allergens'][0],
                        'ServingSize': product['portion_size']}
        nutrition = product['nutritionalInformation']
        nutrition_dict = {}
        for nutrient in nutrition:
            nutrientName = nutrient['title']
            nutrition_dict.update({nutrientName + '_uom': nutrient['units'],
                           nutrientName + '_per100g': nutrient['per100g'],
                           nutrientName + '_perPortion': nutrient['perPortion'],
                           nutrientName + '_percent': nutrient['percent']})
        product_dict.update(nutrition_dict)
        greggs.append(product_dict)

greggs = pd.DataFrame(greggs)
greggs.to_csv(path_greggs + '/greggs_items.csv')
print('Finished Scraping Greggs!')