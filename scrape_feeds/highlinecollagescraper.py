from scrape_handler import site_scrape_execute, SiteScraperResults
from bs4 import BeautifulSoup
from scrape_utils import fetch_page_bypass, transform_elements_to_text


@site_scrape_execute
async def scrape(page: int) -> SiteScraperResults:
    bypass_url = fetch_page_bypass(f'https://highlinealerts.highline.edu/alerts/page/{page}')
    name = 'Highline College'
    soup = BeautifulSoup(bypass_url, 'html.parser')
    titles = soup.find_all('h2', class_='blog-shortcode-post-title entry-title')
    urls = [url.find('a').get('href') for url in titles]
    bodys = [body.find('p').get_text().lower()
             for body in soup.find_all('div', class_='fusion-post-content-container')
             ]
    return SiteScraperResults(name=name, titles=transform_elements_to_text(titles), urls=urls, bodys=bodys)