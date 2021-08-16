import requests
from bs4 import BeautifulSoup as bs
import json
url = 'https://hh.ru'
vacancy_name = input("Enter vacancy name >> ")
pages_count = int(input("How many pages to check? >> "))
print("Loading proxies...")
proxies = []
with open("proxies.txt", 'r') as f:
    for line in f:
        ip = line.rstrip()
        proxy = {
            "http": "http://"+ip,
            "https": "https://"+ip
        }
        proxies.append(proxy)
print("Proxies loaded.")
params = {
    'area': 1,
    'fromSearchLine': 'true',
    'st': 'searchVacancy',
    'text': vacancy_name,
    'page': 0
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}
proxyFinded = False
usefullProxy = None
vacancies_data = []
for page in range(pages_count):
    print("Starting page", page)
    params['page'] = page
    try_num = 0
    pageLoaded = False
    response = None
    if proxyFinded:
        try:
            response = requests.get(url + '/search/vacancy', params=params, headers=headers, proxies=usefullProxy)
            print("Searching url:", response.url)
            if response.status_code == 200:
                print("Page loaded!")
                pageLoaded = True
            else:
                print("Error:The response status code is", response.status_code)
                break
        except Exception as e:
            print("Cannot connect to proxy or website is unavailable! Error:", str(e))
            proxyFinded = False
            usefullProxy = None
    if not proxyFinded:
        for proxy in proxies:
            print("Connecting to proxy", proxy['https'])
            try:
                response = requests.get(url +'/search/vacancy', params=params, headers=headers, proxies=proxy)
                print("Searching url:", response.url)
                if response.status_code == 200:
                    print("Page loaded!")
                    proxyFinded = True
                    usefullProxy = proxy
                    pageLoaded = True
                    break
                else:
                    print("Error:The response status code is", response.status_code)
                    break
            except:
                try_num+=1
                print("Error:Cannot connect to proxy or website is unavailable!")
    if try_num == len(proxies):
        print("Cannot do anything... sorry...")
        break
    if pageLoaded:
        soup = bs(response.text, 'html.parser')
        vacancies = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
        for vacancy in vacancies:
            name_tag = vacancy.find('a', attrs = {'class': 'bloko-link'})
            name = name_tag.getText()
            vacancy_url = name_tag['href']
            sidebar_tag_children = list(vacancy.find('div', attrs = {'class': 'vacancy-serp-item__sidebar'}).children)
            salary = None
            if len(sidebar_tag_children) != 0:
                salary = sidebar_tag_children[0].getText()
            vacancy_data = {
                'vacancy_name': name,
                'vacancy_url': vacancy_url,
                'salary': salary,
                'site': 'hh.ru'
            }
            vacancies_data.append(vacancy_data)
    else:
        print("Are you sure you do everything right?")
        break
with open("vacancies.json", 'w', encoding='utf-8') as f:
    json.dump(vacancies_data, f, ensure_ascii=False)
print("Finished!")