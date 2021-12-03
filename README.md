# Bookscrap
***
Beta version of a scrap application to register books data (price, title, category, picture, ...) from http://books.toscrape.com/
## Technologies
***
* [Windows 10 Professionnel]: Version 21H1
* [Python]: Version 3.9.6
## Installation
***

## Development step
1. [ETL product page](#etl-product-page)
2. [ETL category page](#etl-category-page)
3. [ETL all category and product page](etl-all-category-and-product-page)
4. [ETL picture of product](etl-picture-of-product)
### ETL product page
***
Choose a product page, visit him, extract data below and register it in a CVS file :
- product_page_url
- universal_ product_code (upc)
- title
- price_including_tax
- price_excluding_tax
- number_available
- product_description
- category
- review_rating
- image_url
### ETL category page
***
Choose a category, visit him, extract URL of each product and register product data in CSV file.
### ETL all category and product page
***
Extract all category and all products data of each category and register it in a different CSV file for each category.
### ETL picture of product
***
Download, register and associate picture of each product.