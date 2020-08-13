from bs4 import BeautifulSoup
from datetime import date
import re
from selenium import webdriver
import pandas as pd
import os
import time

# 3. Costa Coffee --> cannot seem to scrape the API, but will try again (add the scripts using selenium for now)
# costa_url = 'https://www.costa.co.uk/api/nutrition/graphql'
# costa_payload = '{"query":"{\n  product(id: 25624) {\n    name\n    id\n    image\n    description\n   \tnutrition {\n      allergens {\n        celery\n        crustacean\n        egg\n        fish\n        lupin\n        milk\n        mollusc\n        mustard\n        nuts {\n          contained\n          sources\n        }\n        peanut\n        sesame\n        soya\n        sulphite\n      }\n      attributes\n      cereals {\n        barley\n        oat\n        rye\n        wheat\n      }\n      containsNuts\n      created\n      dairyFree\n      glutenFree\n      ingredients\n      portion\n      updated\n      vegan\n      vegetarian\n      nutrition {\n        calories\n        carbohydrates\n        fat\n        kilojoules\n        protein\n        salt\n        saturates\n        sugars\n      }\n      nutritionPerPortion {\n        calories\n        carbohydrates\n        fat\n        kilojoules\n        protein\n        salt\n        saturates\n        sugars\n      }\n    }\n  }\n}\n","vars":{}}'
# headers = {'Content-Type':'application/json, text/plain, */*', 'Cookie':'_ga=GA1.3.1012133418.1594691308; _abck=FA49D9447861D78056E1C5633AEC683E~0~YAAQPXv+pS1vDxZzAQAAt00CSwQvc0gITew3AqdLuJWkPcuvSw9AdboLajzbraQeKPfHE6auOe0EZgipS9659jyLCpMbsud58JpJ2OxkvkG2WWmHwTMNbuHBTjpD3EHo8wNjberVavIGEgBuEZW6fHDhcuq/PHJBGrpP3+htqZtACFY2Vr1nIUnLm/ZcFHiThqNHwze714SYgpX49tz6Ltyw24G8MM08yi3qmUuFOHG31U3Qme8Na3W9GvgOUziPwL7WR5Uo4af4RfYbAA9zcxuoXQBARqnixBIQfugdzLf9FI2Kxrf+EjaoJcV9DucglLpN6hgiARA=~-1~||1-rojlzqEdpA-2000-10-1000-2||~-1; costa_cookieconsent=allow; s_fid=2D5370F856DC8EC0-0125BBA38EC3F13C; ak_bmsc=3CA4F155AED2CCA860A4DCED0954A9E31728BE1A264900004833285F4E79F94A~plp3wZ8mbjcPb/cJCim5vNG0S/gQkMam1xI8tR0qb4wEs8sylVQ3uBPvolpaVSzgu90Lk1lELcqv4LtfZe/VsO3OQVrU1KU0VKNkRfdwZxw2sjfXWKaD6C/3pub9ktUYMo6NfjbwsXhu+A+CjvLqDXC1o+zM5chS7lepurnZbVOQGy++Ghjg7hJgB821MW4r+CZeIeSgzecNIBxyjr1GJDTjkZSecNpcSYS5EC8b08HLc=; bm_sz=F092DBD716D13407D52D106097432180~YAAQGr4oF5vWDI1zAQAAMlMItQj6ZVQFKCp40J4BanZTeWco1nbix5xJRTaZGtZUXyfvvTkMOUq8pmzcXR++xZxEhQ/w9Vml86q0FKpuGL9D64+38bjQqmp/z2NV/f857/27oSD3lYXPjpG0EunnydPAmL6V5Qmh9LHek7Xza5H/4rcqIThht9Zb7qcdlD0O2Q==; _gid=GA1.3.1912496952.1596470091; s_cc=true; _gat=1; bm_sv=A0DBE93A81832CC23F558BBFEBC86196~Eq0Yc8gn+KszN+Jzf3/ZsqZJuBv1wni5r7SGrqdQrDFRhLgPu1b99jd557J7jfhdXD86Hvssgk/Pr0RYXuATBD9hXGTG3tb4+aPcruMk2DCLzuMB6C/S+ZP5DXq4HJrSiqid3jfGOAjhurDYwATLOg8K64rKY08LhdtjHftKIQs=; s_sq=costacoffeeprod%3D%2526c.%2526a.%2526activitymap.%2526page%253Dhttps%25253A%25252F%25252Fwww.costa.co.uk%25252Fmenu%25252F%2526link%253DHoneycomb%252520Latte%252520Macchiato%2526region%253Dgatsby-focus-wrapper%2526.activitymap%2526.a%2526.c%2526pid%253Dhttps%25253A%25252F%25252Fwww.costa.co.uk%25252Fmenu%25252F%2526oid%253Dfunctioncn%252528%252529%25257B%25257D%2526oidt%253D2%2526ot%253DDIV',
#            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
#            'Origin':'https://www.costa.co.uk','Referer':'https://www.costa.co.uk/menu/','Content-Length':'1010'}
# requests.post(url,params=costa_payload,headers = headers)
path_costa = './costa_' + date.today().strftime("%b-%d-%Y")
os.mkdir(path_costa)

costa_url = "https://www.costa.co.uk/menu/"
options = webdriver.ChromeOptions()
# options.headless = True  # turn on the headless mode!
browser = webdriver.Chrome("/Users/huangyuru/PycharmProjects/centris.ca/covid/chromedriver83", options=options)
browser.get(costa_url)
time.sleep(2)

# accept cookie
browser.find_element_by_xpath('.//div/button[@data-cy="cookieconsent__btn--accept"]').click()
drink_button = browser.find_elements_by_class_name("productItem__Product-gctefu-0")


def parse_item(page, size=None, milk=None):
    soup = BeautifulSoup(page, 'html.parser')
    product_detail = soup.find_all('div', {'class': 'componentWrapperWhite'})
    product_name = product_detail[0].h1.text if product_detail[0].h1 else product_detail[0].h2.text
    product_description = product_detail[0].p.text if product_detail[0].p else "N/A"
    product_ingredients = soup.find('div', {'class': 'ingredients'}).text if soup.find('div', {
        'class': 'ingredients'}) else "N/A"
    alltables = soup.find_all('table')
    # nutrition information collection
    nutrition_table = alltables[0]
    nutrition_columns = [name.text for name in nutrition_table.findAll('th')]
    nutrition_columns2 = [re.sub('\(.*?\)', '', name) for name in nutrition_columns]
    In_Store = [s for i, s in enumerate(nutrition_columns) if 'In-Store' in s]
    In_Store_column = In_Store[0] if In_Store else 'NA'
    Take_Out = [s for i, s in enumerate(nutrition_columns) if 'Take-Out' in s]
    Take_Out_column = Take_Out[0] if Take_Out else 'NA'
    serving_size_In_Store = In_Store_column[In_Store_column.find("(") + 1:In_Store_column.find(")")]
    serving_size_Take_Out = Take_Out_column[Take_Out_column.find("(") + 1:Take_Out_column.find(")")]
    row_dict = {'Product_Name': product_name, 'Product_Description': product_description,
                'Size': size, 'Milk': milk,
                'Product_Ingredients': product_ingredients}
    for row in nutrition_table.findAll('tr')[1:]:
        text = [item.text for item in row.findAll('td')]
        for i in range(len(text) - 1):
            row_dict.update({text[0] + '_' + nutrition_columns2[i + 1]: text[i + 1]})
    row_dict.update({'ServingSize_In_Store': serving_size_In_Store,
                     'ServingSize_Take_Out': serving_size_Take_Out})
    # allergen table
    allergen_table = alltables[3]
    for row in allergen_table.findAll('tr'):
        text = [item.text for item in row.findAll('td')]
        row_dict.update({text[0]: text[1]})
    # gluten table
    gluten_table = alltables[2]
    for row in gluten_table.findAll('tr'):
        text = [item.text for item in row.findAll('td')]
        row_dict.update({text[0]: text[1]})
    return row_dict


records = []
for drink in drink_button:
    drink.click()
    time.sleep(1)
    sizes = browser.find_elements_by_xpath('//div[@class="filterGroup size"]/button')
    milk_choices = browser.find_elements_by_xpath('//div[@class="filterGroup milk"]/button')
    if len(sizes) > 0:
        for size in sizes:
            size.click()
            if len(milk_choices) > 0:
                for milk in range(len(milk_choices)):
                    milk_choices[milk].click()
                    row = parse_item(page=browser.page_source, milk=milk_choices[milk].text, size=size.text)
                    records.append(row)
            else:
                row = parse_item(page=browser.page_source, size=size.text)
                records.append(row)
    else:
        if len(milk_choices) > 0:
            for milk in range(len(milk_choices)):
                milk_choices[milk].click()
                row = parse_item(page=browser.page_source, milk=milk_choices[milk].text)
                records.append(row)
        else:
            row = parse_item(page=browser.page_source)
            records.append(row)
    close_button = browser.find_element_by_xpath('//button[@class="closeButton"]')
    close_button.click()
    time.sleep(2)

browser.find_elements_by_xpath('//div[@class="pageSelect__StyledPageSelect-k46clq-0 dGJnrT"]/button')[1].click()
food_button = browser.find_elements_by_class_name("productItem__Product-gctefu-0")

for food in range(68, len(food_button)):
    food_button[food].click()
    time.sleep(1)
    row = parse_item(page=browser.page_source)
    records.append(row)
    close_button = browser.find_element_by_xpath('//button[@class="closeButton"]')
    close_button.click()
    time.sleep(1)

costa = pd.DataFrame(records)
costa.to_csv(path_costa + '/costa_items.csv')

print('Finished Scraping Costa Coffee!')