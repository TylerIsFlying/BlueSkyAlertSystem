from scrape_utils import fetch_page_bypass
from bs4 import BeautifulSoup
from scrape_handler import site_scrape_execute
from scrape_handler import SiteScraperResults
import asyncio
from scrape_utils import fetch_page_bypass, transform_elements_to_text


@site_scrape_execute
async def scrape_seattle_feed(page: int) -> SiteScraperResults:
    bypass_url = fetch_page_bypass(f'https://alert.seattle.gov/page/{page}')
    name = 'seattle'
    soup = BeautifulSoup(bypass_url, 'html.parser')
    titles = soup.find_all('h2', class_='entry-title')
    urls = [url.find('a').get('href') for url in titles]
    bodys = [body.find('p').get_text().lower() for body in soup.find_all('div', class_='entry-content')]
    return SiteScraperResults(name, transform_elements_to_text(titles), urls, bodys)

if __name__ == '__main__':
    asyncio.run(scrape_seattle_feed(0))
