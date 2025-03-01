import cloudscraper


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


def transform_elements_to_text(elements) -> []:
    element_list = [element.get_text().lower() for element in elements]
    return element_list
