from unittest.mock import AsyncMock

import aiohttp
import pytest

from src.parsers.excel_parser import parse_xls_content, parse_xls_data
from src.parsers.html_parser import extract_links_from_page, fetch_page_html
from src.parsers.url_collector import collect_all_trade_links


def test_parse_xls_content_with_invalid_data():
    invalid_content = b""
    with pytest.raises(Exception):
        parse_xls_content(invalid_content, "2024-10-26")


@pytest.mark.asyncio
async def test_parse_xls_data(mocker, sample_xls_content, sample_date):
    mocker.patch(
        "src.parsers.excel_parser.parse_xls_content",
        return_value=[
            (
                "Товар",
                "Наименование",
                "Това",
                "р1",
                None,
                "1",
                1000,
                200,
                1,
                sample_date,
            )
        ],
    )
    result = await parse_xls_data(sample_xls_content, sample_date)

    assert result == [
        ("Товар", "Наименование", "Това", "р1", None, "1", 1000, 200, 1, sample_date)
    ]


@pytest.mark.asyncio
async def test_fetch_page_html_success(mocker):
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.text = AsyncMock(
        return_value="<html><body>Test Content</body></html>"
    )

    mock_session = mocker.patch("aiohttp.ClientSession.get", return_value=mock_response)
    mock_session().__aenter__.return_value = mock_response

    url = "https://example.com"
    result = await fetch_page_html(url)

    assert result == "<html><body>Test Content</body></html>"
    mock_response.text.assert_called_once()


@pytest.mark.asyncio
async def test_fetch_page_html_client_error(mocker):
    mock_session = mocker.patch(
        "aiohttp.ClientSession.get", side_effect=aiohttp.ClientError("Request failed")
    )
    url = "https://example.com"

    with pytest.raises(aiohttp.ClientError):
        await fetch_page_html(url)
    mock_session.assert_called_once_with(url)


@pytest.mark.asyncio
async def test_extract_links_from_page_success(mocker):
    mock_html_content = """
    <html>
        <body>
            <a class="accordeon-inner__item-title link xls" href="/link1">Link 1</a>
            <div class="accordeon-inner__item-inner__title"><span>01.01.2024</span></div>
            <a class="accordeon-inner__item-title link xls" href="/link2">Link 2</a>
            <div class="accordeon-inner__item-inner__title"><span>01.01.2023</span></div>
        </body>
    </html>
    """
    mocker.patch(
        "src.parsers.html_parser.fetch_page_html", return_value=mock_html_content
    )
    mocker.patch("src.utils.validator.is_valid_year", return_value=True)

    url = "https://example.com"
    links_data, has_invalid_date = await extract_links_from_page(url)

    expected_links = [
        ("https://spimex.com/link1", "01.01.2024"),
        ("https://spimex.com/link2", "01.01.2023"),
    ]

    assert links_data == expected_links
    assert not has_invalid_date


@pytest.mark.asyncio
async def test_collect_all_trade_links(mocker):
    mocker.patch(
        "src.parsers.url_collector.extract_links_from_page",
        side_effect=[
            (
                [
                    (f"https://spimex.com/file{i}.xls", f"2024-01-0{i}")
                    for i in range(1, 5)
                ],
                False,
            ),
            ([], True),
        ],
    )
    links = await collect_all_trade_links()
    assert len(links) > 0
    assert all(isinstance(link, tuple) for link in links)
