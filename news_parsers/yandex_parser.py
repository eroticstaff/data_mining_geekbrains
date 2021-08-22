from lxml import html
import requests

def parse_yandex_news(url, headers):
    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)
    main = dom.xpath("//div[@class='mg-grid__col mg-grid__col_xs_12 mg-grid__col_sm_9']")[0]
    rubrics_names = ['Главные новости']
    rubrics_names.extend(main.xpath(".//div[contains(@class,'heading-wrapper')]//h1//text()"))
    top_news = main.xpath(".//div[contains(@class, 'news-top-flexible-stories')]")[0]
    rubrics = main.xpath(".//div[contains(@class,'mg-top-rubric-flexible-stories')]")
    all_news_by_rubrics = []
    top_news_data = yandex_parse_rubric(top_news)
    all_news_by_rubrics.append(top_news_data)
    for rubric in rubrics:
        news = yandex_parse_rubric(rubric)
        all_news_by_rubrics.append(news)
    return (rubrics_names, all_news_by_rubrics)

def yandex_parse_rubric(rubric):
    rubric_news = []
    news = rubric.xpath('.//div[contains(@class,"mg-grid__col")]')
    for new in news:
        subnews = new.xpath('.//div[contains(@class,"mg-grid__col")]')
        if len(subnews) == 0:
            new_data = {}
            name = new.xpath(".//a//h2//text()")
            url = new.xpath(".//a/@href")[0]
            source = new.xpath(".//span[contains(@class,'mg-card-source__source')]//text()")
            time = new.xpath(".//span[contains(@class,'mg-card-source__time')]//text()")
            new_data['name'] = name[0]
            new_data['url'] = url
            new_data['time'] = time[0]
            new_data['source'] = source[0]
            rubric_news.append(new_data)
        else:
            rubric_news.extend(yandex_parse_rubric(new))
            break
    return rubric_news