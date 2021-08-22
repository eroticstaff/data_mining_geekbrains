from news_parsers.yandex_parser import parse_yandex_news
from news_parsers.lenta_parser import parse_lenta_news
from pprint import pprint
from pymongo import MongoClient

def print_news(news):
    for new in news:
        print("-"*10)
        print(new['name'])
        print(new['url'])
        print(new['source'])
        print(new['time'])
def write_news_to_db(news):
    for new in news:
        news_db.insert_one(new)
yandex_url = 'https://yandex.ru/news'
lenta_url = 'https://lenta.ru/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
client = MongoClient("127.0.0.1", 27017)
db = client['news']
news_db = db.news
news_db.delete_many({})


lenta_news = parse_lenta_news(lenta_url, headers)
write_news_to_db(lenta_news)
print("/" * 40)
print("/" * 40)
print("ЛЕНТА.РУ")
print("/" * 40)
print("/" * 40)
print_news(lenta_news)
yandex_rubric_names, yandex_news_by_rubric = parse_yandex_news(yandex_url, headers)
print("/" * 40)
print("/" * 40)
print("ЯНДЕКС")
print("/" * 40)
print("/" * 40)

for rubric_name, rubric_news in zip(yandex_rubric_names, yandex_news_by_rubric):
    print("=" * 30)
    print(rubric_name)
    print("=" * 30)
    print_news(rubric_news)
    write_news_to_db(rubric_news)