from bs4 import BeautifulSoup
from scrape_utils import fetch_page_bypass, transform_elements_to_text
import asyncio
from scrape_handler import site_scrape_execute, SiteScraperResults


@site_scrape_execute
async def scrape_la_feed(page: int) -> SiteScraperResults:
    """Scrapes the results from the la alerts site"""
    # Starts on la at 0th page
    base_url = f'https://lafd.org/alerts?page={page - 1}'
    name = 'los angeles'
    bypass_url = fetch_page_bypass(base_url)
    soup = BeautifulSoup(bypass_url, 'html.parser')

    titles = soup.find_all("h2", class_="alert-node-title")
    urls = get_url(titles)
    bodys = transform_elements_to_text(soup.find_all("div", class_="alert-node-body"))
    return SiteScraperResults(name=name, titles=transform_elements_to_text(titles), urls=urls, bodys=bodys)


def get_url(url_objects):
    url_objects_list = ["https://lafd.org" + url_object.find('a').get('href') for url_object in url_objects]
    return url_objects_list


if __name__ == '__main__':
    asyncio.run(scrape_la_feed(0))
