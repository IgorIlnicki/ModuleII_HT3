import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://us:us1@cluster0.g6s22by.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.quot

# Функція для отримання даних зі сторінки
def get_page(url):
    response = requests.get(url)
    return response.text

def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    quotes = []
    authors = {}

    # Парсимо цитати
    for quote in soup.find_all('div', class_='quote'):
        text = quote.find('span', class_='text').text
        author_link = quote.find('a', href=True)
        author_name = quote.find('small', class_='author').text
        author_url = urljoin(BASE_URL, author_link['href'])

        # Перевіряємо, чи ми вже отримали інформацію про цього автора
        if author_name not in authors:
            # Отримуємо додаткову інформацію про автора
            author_page = get_page(author_url)
            author_soup = BeautifulSoup(author_page, 'html.parser')
            born_date = author_soup.find('span', class_='author-born-date').text
            born_location = author_soup.find('span', class_='author-born-location').text
            description = author_soup.find('div', class_='author-description').text.strip()

            # Зберігаємо інформацію про автора
            authors[author_name] = {
                'fullname': author_name,
                'born_date': born_date,
                'born_location': born_location,
                'description': description
            }
            try:
                db.authors.insert_one(authors[author_name])
            except Exception as e:
                print(e)
        tags = [tag.text for tag in quote.find_all('a', class_='tag')]
        quotes.append({'quote': text, 'author': author_name, 'tags': tags})  
        try:
            db.qoutes.insert_one({'quote': text, 'author': author_name, 'tags': tags})
        except Exception as e:
            print(e)
    return quotes, authors

# Базовий URL сайту
BASE_URL = 'http://quotes.toscrape.com'

# Основна функція скрапінгу
def scrape_quotes(url):
    all_quotes = []
    all_authors = {}

    while url:
        html = get_page(url)
        quotes, authors = parse_page(html)
        all_quotes.extend(quotes)

        for author_name, author_data in authors.items():
            if author_name not in all_authors:
                all_authors[author_name] = author_data


        soup = BeautifulSoup(html, 'html.parser')
        next_page = soup.find('li', class_='next')
        if next_page:
            url = urljoin(BASE_URL, next_page.find('a')['href'])
        else:
            url = None
    # Збереження даних у JSON файли
    with open('quotes.json', 'w', encoding='utf-8') as f:
        json.dump(all_quotes, f, ensure_ascii=False, indent=2)

    with open('authors.json', 'w', encoding='utf-8') as f:
        json.dump(list(all_authors.values()), f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    scrape_quotes(BASE_URL)