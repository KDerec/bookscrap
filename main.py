import os
import csv
import requests
from bs4 import BeautifulSoup

os.chdir(os.getcwd() + '\data\csv')

home_page = 'https://books.toscrape.com/index.html'


def create_new_csv(self):
    page = requests.get(self).content
    soup = BeautifulSoup(page, 'html.parser')
    
    category = soup.find_all('a')[3].text
    columns_name = ('product_page_url', 'universal_product_code', 'title', 
                    'price_including_tax', 'price_excluding_tax', 
                    'number_available', 'product_description', 'category', 
                    'review_rating', 'image_url')
    filename = '{}.csv'.format(category)

    with open(filename, 'w', encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(columns_name)

    return category

def extract_product_data_in_csv(self):
    for url in self:
        page = requests.get(url).content
        soup = BeautifulSoup(page, 'html.parser')

        product_page_url = url
        universal_product_code = soup.find_all('td')[0].text
        title = soup.h1.text
        price_including_tax = soup.find_all('td')[3].text.replace('£','')
        price_excluding_tax = soup.find_all('td')[2].text.replace('£','')
        number_available = soup.find_all('td')[-2].text
        number_available = ''.join(i for i in number_available if i.isdigit())
        product_description = soup.h2.next_sibling.next_element.next_element.text
        category = soup.find_all('a')[3].text
        review_rating = soup.find(class_='star-rating')
        review_rating = review_rating.get('class')[1]
        image_url = 'http://books.toscrape.com/' + soup.img['src'][6:]

        data = [product_page_url, universal_product_code, title, 
        price_including_tax, price_excluding_tax, number_available, 
        product_description, category, review_rating, image_url]

        filename = '{}.csv'.format(category)
        with open(filename, 'a', encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data)

def check_next_page(self):
    page = requests.get(self).content
    soup = BeautifulSoup(page, 'html.parser')

    next_exist = soup.find(class_='next')
    if next_exist:
        result = ''
        while result != '/':
            self, result = self[:-1], self[-1]
        
        new_url = self + result + next_exist.a['href']

        return new_url

def create_product_url_list_of_a_category(self):
    page = requests.get(self).content
    soup = BeautifulSoup(page, 'html.parser')

    for link in soup.find_all('h3'):
        product_url = ('http://books.toscrape.com/catalogue' 
                       + link.find('a').get('href')[8:])
        product_url_list.append(product_url)
    
    new_url = check_next_page(self)
    if new_url:
        create_product_url_list_of_a_category(new_url)

    return product_url_list

def create_category_url_list(self):
    page = requests.get(self).content
    soup = BeautifulSoup(page, 'html.parser')

    for link in soup.find(class_='nav nav-list').ul.find_all('li'):
        category_url = ('http://books.toscrape.com/catalogue' 
                       + link.find('a').get('href')[9:])
        category_url_list.append(category_url)
    
    return category_url_list


category_url_list = []
category_url_list = create_category_url_list(home_page)

for url in category_url_list:
    product_url_list = []
    product_url_list = create_product_url_list_of_a_category(url)
    category = create_new_csv(product_url_list[0])
    extract_product_data_in_csv(product_url_list)
    print('Traitement de la catégorie "{}" terminée.'.format(category))