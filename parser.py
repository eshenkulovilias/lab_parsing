import requests
from bs4 import BeautifulSoup
import pandas as pd


class Writer:
    def __init__(self, res):
        self.depDF = pd.DataFrame(
            {
                'title': res.titles,
                'link': res.links,
                'category': res.categories
            }
        )

    def write_to_csv(self):
        csv_file_contents = self.depDF.to_csv(index=False)
        with open("kivano.csv", "a", encoding='utf-8') as f:
            f.write(csv_file_contents)


class Result:
    def __init__(self, ads):
        self.ads = ads
        self.titles = []
        self.links = []
        self.categories = []
        for ad in ads:
            self.titles.append(ad.title)
            self.links.append(ad.link)
            self.categories.append(ad.category)


class Ad:
    def __init__(self, title, link, category):
        self.title = title
        self.link = link
        self.category = category


def get_html(url):
    r = requests.get(url)
    return r.text


def get_ads(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    ads = soup.find('div', class_='list-view').find_all_next('div', class_='item')
    ads_list = []
    for ad in ads:
        try:
            title = ad.find('div', class_='listbox_title').text.replace('\n', '')
            # print(title)
        except:
            title = 'Нет заголовка'
        try:
            link = url + ad.find('div', class_='listbox_title').find_next('a').get('href')
        except:
            link = ''
        try:
            category = soup.find('div', class_='product-index').find_next('div', class_='portlet-title').find_next('ul', class_='breadcrumb2').find_all_next('li', itemprop='itemListElement')[-1].text
        except:
            category = ''
        ads_list.append(Ad(title, link, category))
    return ads_list


def app(url):
    page_part = '?page='
    for i in range(1, 4):
        url_gen = url + page_part + str(i)
        r = Result(get_ads(get_html(url_gen), url))
        w = Writer(r)
        w.write_to_csv()


def main():
    url1 = 'https://www.kivano.kg/noutbuki'
    app(url1)
    url2 = 'https://www.kivano.kg/planshety'
    app(url2)
    url3 = 'https://www.kivano.kg/besprovodnye-naushniki-i-bluetooth-garnitury'
    app(url3)
    url4 = 'https://www.kivano.kg/kolonki-portativnye'
    app(url4)
    # get_ads(get_html(url1), url1)


main()
