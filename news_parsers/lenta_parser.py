from lxml import html
import requests

def parse_lenta_news(url, headers):
    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)
    news_block = dom.xpath("//section[contains(@class,'js-top-seven')]")[0]
    return parse_parts(news_block)
def parse_parts(news_block):
    news = []
    parts = news_block.xpath(".//div[contains(@class,'span4')]")
    for part in parts:
        items = part.xpath(".//div[contains(@class,'item')]")
        for item in items:
            new = {}
            h2_check = item.xpath(".//h2")
            if len(h2_check) == 0:
                url = "https://lenta.ru"+item.xpath(".//a/@href")[0]
                name = item.xpath(".//a/text()")[0]
                time = item.xpath(".//a/time/@datetime")[0]
                source = "lenta.ru"
            else:
                url = "https://lenta.ru"+h2_check[0].xpath(".//a/@href")[0]
                name = h2_check[0].xpath("./a/text()")[0]
                time = h2_check[0].xpath(".//time/@datetime")[0]
                source = "lenta.ru"
            new['url'] = url
            new['name'] = name
            new['time'] = time
            new['source'] = source
            news.append(new)
    return news