import os

import httpx

from app.schemas.book import BookDetail, BookSearchResponse, BookSummary

GOOGLE_BOOKS_API_BASE = "https://www.googleapis.com/books/v1"


def _extract_isbn(identifiers: list[dict[str, str]] | None) -> str | None:
    if not identifiers:
        return None
    isbn13 = next((i["identifier"] for i in identifiers if i["type"] == "ISBN_13"), None)
    if isbn13:
        return isbn13
    return next((i["identifier"] for i in identifiers if i["type"] == "ISBN_10"), None)


def _parse_summary(item: dict) -> BookSummary:
    info = item.get("volumeInfo", {})
    return BookSummary(
        id=item.get("id", ""),
        title=info.get("title", ""),
        authors=info.get("authors"),
        thumbnail=info.get("imageLinks", {}).get("thumbnail"),
        published_date=info.get("publishedDate"),
        description=info.get("description"),
    )


def _parse_detail(item: dict) -> BookDetail:
    info = item.get("volumeInfo", {})
    return BookDetail(
        id=item.get("id", ""),
        title=info.get("title", ""),
        authors=info.get("authors"),
        thumbnail=info.get("imageLinks", {}).get("thumbnail"),
        published_date=info.get("publishedDate"),
        description=info.get("description"),
        page_count=info.get("pageCount"),
        categories=info.get("categories"),
        publisher=info.get("publisher"),
        isbn=_extract_isbn(info.get("industryIdentifiers")),
    )


async def search_books(q: str, limit: int, offset: int) -> BookSearchResponse:
    api_key = os.environ["GOOGLE_BOOKS_API_KEY"]
    params = {
        "q": q,
        "startIndex": offset,
        "maxResults": limit,
        "key": api_key,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{GOOGLE_BOOKS_API_BASE}/volumes", params=params)
        response.raise_for_status()
        data = response.json()

    items = [_parse_summary(item) for item in data.get("items", [])]
    return BookSearchResponse(
        total=data.get("totalItems", 0),
        limit=limit,
        offset=offset,
        items=items,
    )


async def get_book(book_id: str) -> BookDetail | None:
    api_key = os.environ["GOOGLE_BOOKS_API_KEY"]
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GOOGLE_BOOKS_API_BASE}/volumes/{book_id}",
            params={"key": api_key},
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        data = response.json()

    return _parse_detail(data)
