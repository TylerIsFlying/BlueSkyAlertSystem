import cloudscraper
from bs4 import BeautifulSoup
from scrape_handler import site_scrape_execute
from scrape_handler import SiteScraperResults
import asyncio


def fetch_page_bypass(url):
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)

    coi: int = 1
    # Repsonse code from website: 200 means that the website returned a successful response
    if response.status_code == 200:
        return response.content
    else:
        print(f'Page failed to load, resposne code{response.status_code}')
        return None


@site_scrape_execute
async def scrape_seattle_feed(page: int) -> SiteScraperResults:
    bypass_url = fetch_page_bypass(f'https://alert.seattle.gov/page/{page}')
    name = 'seattle'
    soup = BeautifulSoup(bypass_url, 'html.parser')
    titles = soup.find_all('h2', class_='entry-title')
    urls = [url.find('a').get('href') for url in titles]
    bodys = [body.find('p').get_text().lower() for body in soup.find_all('div', class_='entry-content')]
    return SiteScraperResults(name, transform_elements_to_text(titles), urls, bodys)


def transform_elements_to_text(elements) -> []:
    element_list = [element.get_text().lower() for element in elements]
    return element_list


if __name__ == '__main__':
    asyncio.run(scrape_seattle_feed(0))
