import time

from atproto import Client
from atproto import client_utils
import asyncio
from atproto_client.request import Response
from dotenv import load_dotenv
import os
from scrape_handler import SiteScrapeReceiver
from scrape_handler import SiteScraperResult
from itertools import chain


async def main():
    client = Client()
    load_dotenv()
    username = os.getenv('CLIENT_USERNAME')
    password = os.getenv('CLIENT_PASSWORD')
    client.login(username, password)

    # use -1 if you don't want a limit
    max_posts_before_purge = 100

    data = await scrape_at_index(1, 'scrape_feeds')
    feed = client.get_author_feed(actor=username)
    posts = await get_all_posts(feed)

    if len(posts) >= max_posts_before_purge:
        await purge_posts(client, feed)

    for d in data:
        text_build = client_utils.TextBuilder()
        text_build.text(f'Alert ')
        text_build.text(f"({d.get_name().title()}): ")
        text_build.link(d.get_title().title(), d.get_url().title())
        # BlueSky has character limit of 300
        if len(text_build.build_text()) > 300:
            continue
        if not str(text_build.build_text()) in posts:
            client.send_post(text_build)


async def purge_posts(client: Client, feed: Response):
    for post in feed['feed']:
        client.delete_post(post['post']['uri'])


async def scrape_at_index(page: int, path_name: str, all_content=False) -> list[SiteScraperResult]:
    await SiteScrapeReceiver.register(path_name)
    scrapes = await SiteScrapeReceiver.load_results(page=page)
    if all_content:
        scrapes_combined = list(chain.from_iterable([scrape.make_single_results() for scrape in scrapes]))
        return scrapes_combined
    else:
        return [scrape.make_single_results()[0] for scrape in scrapes]


async def get_all_posts(feed: Response) -> list[str]:
    return [post['post']['record']['text'] for post in feed['feed']]


if __name__ == '__main__':
    asyncio.run(main())
