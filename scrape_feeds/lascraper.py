import requests
from bs4 import BeautifulSoup
import cloudscraper
import asyncio
import feedparser
from scrape_handler import site_scrape_execute
from scrape_handler import SiteScraperResults


# Initial Bypass method using cloudscrapper
def fetch_page_bypass(url):
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)

    coi: int = 1
    # Response code from website: 200 means that the website returned a successful response
    if response.status_code == 200:
        return response.content
    else:
        print(f'Page failed to load, resposne code{response.status_code}')
        return None


@site_scrape_execute
async def scrape_la_feed(page: int):
    # Starts on la at 0th page
    base_url = f'https://lafd.org/alerts?page={page + 1}'
    name = 'los angeles'
    bypass_url = fetch_page_bypass(base_url)
    soup = BeautifulSoup(bypass_url, 'html.parser')

    titles = soup.find_all("h2", class_="alert-node-title")
    urls = get_url(titles)
    bodys = transform_elements_to_text(soup.find_all("div", class_="alert-node-body"))
    return SiteScraperResults(name=name, titles=transform_elements_to_text(titles), urls=urls, bodys=bodys)


def transform_elements_to_text(elements) -> []:
    element_list = [element.get_text().lower() for element in elements]
    return element_list


def get_url(url_objects):
    url_objects_list = ["https://lafd.org" + url_object.find('a').get('href') for url_object in url_objects]
    return url_objects_list


def rss_feed():
    rss_url = 'https://lafd.org/alerts-rss.xml'
    bypass_url = fetch_page_bypass(rss_url)
    feed = feedparser.parse(bypass_url)
    data = {'title': [], 'url': [], 'body': []}
    for entrie in feed.entries:
        soup = BeautifulSoup(entrie.title, 'html.parser')
        data['title'].append(soup.find('a').get_text())
        data['url'].append(soup.find('a').get('href'))
        data['body'].append(entrie.description)
    print(data['body'][0])
    return feed.entries


if __name__ == '__main__':
    asyncio.run(scrape_la_feed(0))
