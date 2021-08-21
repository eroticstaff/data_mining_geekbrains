from pymongo import MongoClient
import json
from pprint import pprint

with open("vacancies.json", 'r', encoding="utf-8") as f:
    data = json.loads(f.read())
host = "127.0.0.1"
port = 27017
client = MongoClient(host=host, port=port)
db = client["vacancies"]
hh = db.headhunter
#hh.delete_many({})
db_data = hh.find({})  #Вместо того, чтобы постоянно обращаться к базе данных для проверки на наличие данной вакансиии - обращусь один раз
for item_data in data:
    finded = False
    for item in db_data:
        if item['vacancy_url'] == item_data['vacancy_url']:
            finded = True
            print("There is already this item in the database!")
            break
    if not finded:
        hh.insert_one(item_data)
price = int(input("Enter (>)price: "))
print("Vacancies with salary greater than " + str(price))
for item in hh.find({"$or": [{"salary.min-salary": {"$gt": price}}, {'salary.max-salary': {"$lt": price}}]}):
    pprint(item)
