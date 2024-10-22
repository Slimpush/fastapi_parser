import logging

import aiohttp
from bs4 import BeautifulSoup
from utils.validator import is_valid_year


async def fetch_page_html(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.text()
        except aiohttp.ClientError as e:
            logging.error(f"Ошибка при запросе {url}: {e}")
            raise


async def extract_links_from_page(url: str):
    html_content = await fetch_page_html(url)
    soup = BeautifulSoup(html_content, "html.parser")

    links_data = []
    for link, div in zip(
        soup.find_all("a", class_="accordeon-inner__item-title link xls")[:10],
        soup.find_all("div", class_="accordeon-inner__item-inner__title")[:10],
    ):
        href = f'https://spimex.com{link.get("href")}'
        date = div.find("span").get_text(strip=True)

        if not is_valid_year(date):
            return links_data, True
        links_data.append((href, date))

    return links_data, False
