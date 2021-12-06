import os
import csv
import requests
from bs4 import BeautifulSoup

category_url = 'http://books.toscrape.com/catalogue/category/books/default_15/index.html'
product_url_list = []

def extract_product_data_in_csv():
    url = 'http://books.toscrape.com/catalogue/soumission_998/index.html'
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')

    product_page_url = url
    universal_product_code = soup.find_all('td')[0].text
    title = soup.h1.text
    price_including_tax = soup.find_all('td')[3].text.replace('Â', '').replace('£','')
    price_excluding_tax = soup.find_all('td')[2].text.replace('Â', '').replace('£','')
    number_available = soup.find_all('td')[-2].text
    number_available = ''.join(i for i in number_available if i.isdigit())
    product_description = soup.h2.next_sibling.next_element.next_element.text
    category = soup.find_all('a')[3].text
    review_rating = soup.find(class_='star-rating')
    review_rating = review_rating.get('class')[1]
    image_url = soup.img['src']
    image_url = 'http://books.toscrape.com/' + image_url

    #Création du fichier csv
    os.chdir(os.getcwd() + '\data\csv')
    columns_name = ('product_page_url', 'universal_product_code', 'title', 
                    'price_including_tax', 'price_excluding_tax', 
                    'number_available', 'product_description', 'category', 
                    'review_rating', 'image_url')
    data = [product_page_url, universal_product_code, title, 
            price_including_tax, price_excluding_tax, number_available, 
            product_description, category, review_rating, image_url]
    filename = '{}.csv'.format(title)
    with open(filename, 'w', encoding="utf-8", newline='') as new:
        writer = csv.writer(new)
        writer.writerow(columns_name)
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


product_url_list = create_product_url_list_of_a_category(category_url)
extract_product_data_in_csv(product_url_list)