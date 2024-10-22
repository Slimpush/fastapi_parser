import logging

from parsers.html_parser import extract_links_from_page


async def collect_all_trade_links():
    page_num = 1
    all_links = []

    while True:
        url = (
            f"https://spimex.com/markets/oil_products/trades/results/?"
            f"page=page-{page_num}"
        )
        try:
            links, stop = await extract_links_from_page(url)
            all_links.extend(links)
            page_num += 1
            if stop:
                break
        except Exception as e:
            logging.error(f"Ошибка на странице {url}: {e}")
            break

    return all_links
