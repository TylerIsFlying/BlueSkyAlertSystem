from atproto import Client
from atproto import client_utils
import asyncio
from dotenv import load_dotenv
import os
from scrape import SiteScrapeReceiver
from scrape import SiteScraperResults
from scrape import SiteScraperResult
async def main():
    client = Client()
    load_dotenv()
    username = os.getenv('CLIENT_USERNAME')
    password = os.getenv('CLIENT_PASSWORD')
    client.login(username, password)

    text_build = client_utils.TextBuilder()
    text_build.text(f'Alert ')
    data = await scrape_at_index(1,1)

    text_build.text(f"({data.get_name().title()}): ")
    text_build.link(data.get_title().title(), data.get_url().title())
    client.send_post(text_build)


async def scrape_at_index(page: int, index: int) -> {}:
    await SiteScrapeReceiver.register('scrape_feeds')
    scrapes = await SiteScrapeReceiver.load_results(page=page)

    return scrapes[index].make_single_results()[index]


if __name__ == '__main__':
    asyncio.run(main())
