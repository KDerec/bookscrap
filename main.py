import os
import csv
import requests
from bs4 import BeautifulSoup


path = os.getcwd()
home_page = 'https://books.toscrape.com/index.html'


def test_page(self):
    while True:
        try:
            page = requests.get(self, timeout=6)
            page.raise_for_status()
            break
        except requests.models.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            decide_to_quit()
        except requests.exceptions.Timeout:
            print('The request timed out')
            decide_to_quit()
        except Exception as err:
            print(f'Error occurred: {err}')
            decide_to_quit()

    return page

def decide_to_quit():
    choix = input('Recommencer ou quitter ? Tapez \'q\' pour quitter. ')
    if choix.upper() != 'Q':
        pass
    else:
        quit()

def parse_html(self):
    page = test_page(self)
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup

def create_category_url_list(self):
    soup = parse_html(self)

    for link in soup.find(class_='nav nav-list').ul.find_all('li'):
        category_url = ('http://books.toscrape.com/catalogue' 
                       + link.find('a').get('href')[9:])
        category_url_list.append(category_url)

    return category_url_list

def create_product_url_list_of_a_category(self):
    soup = parse_html(self)

    for link in soup.find_all('h3'):
        product_url = ('http://books.toscrape.com/catalogue' 
                       + link.find('a').get('href')[8:])
        product_url_list.append(product_url)
    
    new_url = check_next_page(self)
    if new_url:
        create_product_url_list_of_a_category(new_url)

    return product_url_list

def check_next_page(self):
    soup = parse_html(self)

    next_exist = soup.find(class_='next')
    if next_exist:
        result = ''
        while result != '/':
            self, result = self[:-1], self[-1]
        
        new_url = self + result + next_exist.a['href']

        return new_url

def create_new_csv(self):
    soup = parse_html(self)
    
    category = soup.find_all('a')[3].text
    columns_name = ('product_page_url', 'universal_product_code', 'title', 
                    'price_including_tax', 'price_excluding_tax', 
                    'number_available', 'product_description', 'category', 
                    'review_rating', 'image_url')
    filename = '{}.csv'.format(category)

    with open(filename, 'w', encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(columns_name)
    
    try:
        os.mkdir(path + '\data\images\\' + category)
    except FileExistsError:
        pass   

    return category

def extract_product_data_in_csv(self):
    for url in self:
        soup = parse_html(url)
        table = soup.find(class_='table table-striped')

        product_page_url = url
        title = soup.h1.text
        universal_product_code = table.find(text='UPC').next_element.text
        price_including_tax = table.find(text='Price (incl. tax)').next_element
        price_including_tax = price_including_tax.text.replace('£','')
        price_excluding_tax = table.find(text='Price (excl. tax)').next_element
        price_excluding_tax = price_excluding_tax.text.replace('£','')
        number_available = soup.find(class_='instock availability').text.strip()
        number_available = ''.join(i for i in number_available if i.isdigit())
        product_description = soup.head.find('meta', attrs={'name':'description'})
        product_description = product_description.attrs['content'].strip()
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
        
        title = formate_file_name_for_windows(title)
        download_image(image_url, title, category)

def formate_file_name_for_windows(self):
    self = self.replace("<","").replace(">","").replace(":"," ").replace("«","")
    self = self.replace("»","").replace("|","").replace("?","").replace("*","")
    self = self.replace("."," ").replace('"',"").replace('/'," ").rstrip()

    return self

def download_image(image_url, title, category):
    os.chdir(path + '\data\images\\' + category)
    images = test_page(image_url)
    open('{}.jpg'.format(title), 'wb').write(images.content)
    os.chdir(path + '\data\csv')


print('Bienvenue dans l\'application Bookscrap !')

choix = input('Démarrer l\'extraction des données ? Tapez \'q\' pour quitter.')

if choix.upper() != 'Q':
    print('''
Vérification des dossiers nécessaires et démarrage de l'extraction des données
du site books.toscrape.com...
''')
    try:
        os.mkdir(path + '\data')
        os.mkdir(path + '\data\csv')
        os.mkdir(path + '\data\images')
    except FileExistsError:
        pass
    else:
        print('\nDossiers data, csv et images créés.')

    os.chdir(path + '\data\csv')
    category_url_list = []
    category_url_list = set(create_category_url_list(home_page))

    for url in category_url_list:
        product_url_list = []
        product_url_list = create_product_url_list_of_a_category(url)
        category = create_new_csv(product_url_list[0])
        print('\nTraitement de la catégorie "{}" en cours...'.format(category))
        extract_product_data_in_csv(product_url_list)
        print('Traitement de la catégorie "{}" terminé.'.format(category))

input('\nFin du programme.\nAppuyer sur une touche pour quitter :')
quit()