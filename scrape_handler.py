import inspect
import pkgutil
import importlib


class SiteScraperResult:
    def __init__(self, name: str, title: str, url: str, body: str):
        self.name = name
        self.title = title
        self.url = url
        self.body = body

    def get_title(self):
        return self.title.lower()

    def get_name(self):
        return self.name.lower()

    def get_url(self):
        return self.url.lower()

    def get_body(self):
        return self.body.lower()

    def __repr__(self):
        name = f'name: {self.get_name()}\n'
        title = f'title: {self.get_title()}\n'
        url = f'url: {self.get_url()}\n'
        body = f'body: {self.get_body()}\n'

        return name + title + url + body


class SiteScraperResults:
    def __init__(self, name: str, titles: [str], urls: [str], bodys: [str]):
        self.name = name
        self.titles = titles
        self.urls = urls
        self.bodys = bodys

    def get_titles(self):
        return self.titles

    def get_name(self):
        return self.name.lower()

    def get_urls(self):
        return self.urls

    def get_bodys(self):
        return self.bodys

    def make_single_results(self) -> list[SiteScraperResult]:
        """Converts a SiteScraperResults to list of SiteScraperResult"""
        max_length = max(len(self.titles), len(self.urls), len(self.bodys))

        results = []

        for index in range(max_length):
            results.append(SiteScraperResult(
                name=self.name
                , title=self.titles[index] if index < len(self.titles) else None
                , url=self.urls[index] if index < len(self.urls) else None
                , body=self.bodys[index] if index < len(self.bodys) else None
            ))
        return results

    def __repr__(self):
        name = f'name: {self.get_name()}\n'
        title = f'title: {self.get_titles()}\n'
        url = f'url: {self.get_urls()}\n'
        body = f'body: {self.get_bodys()}\n'
        return name + title + url + body


registered_scraper_results = []


def site_scrape_execute(func):
    """Decorator to register scrape function"""
    registered_scraper_results.append(func)


class SiteScrapeReceiver:
    @staticmethod
    async def load_results(*args, **kwargs) -> list[SiteScraperResults]:
        """Executes all decorated functions and gets SiteScraperResults instances."""
        results = []

        for func in registered_scraper_results:
            result = await func(*args, **kwargs)
            # Could have a scraper function that returns a list of SiteScraperResult so we combine it.
            if isinstance(result, list) and all(isinstance(r, SiteScraperResults) for r in result):
                results.extend(result)
            elif isinstance(result, SiteScraperResults):
                results.append(result)
            else:
                raise ValueError(f"Function {func.__name__} must return a SiteScraperResults or list of it.")

        return results

    @staticmethod
    async def load_result(*args, **kwargs) -> list[SiteScraperResult]:
        """Executes all decorated functions and gets SiteScraperResult instances."""
        results = []

        for func in registered_scraper_results:
            result = func(*args, **kwargs)
            # Could have a scraper function that returns a list of SiteScraperResult so we combine it.
            if isinstance(result, list) and all(isinstance(r, SiteScraperResult) for r in result):
                results.extend(result)
            elif isinstance(result, SiteScraperResult):
                results.append(result)
            else:
                raise ValueError(f"Function {func.__name__} must return a SiteScraperResult or list of it.")

        return results

    @staticmethod
    async def register(module_name: str):
        """Imports dynamically all modules in a package decorated with @site_scrape_execute"""
        package = importlib.import_module(module_name)
        for _, module_name, _ in pkgutil.iter_modules(package.__path__):
            importlib.import_module(f"{package.__name__}.{module_name}")
