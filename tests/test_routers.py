from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.book import BookDetail, BookSearchResponse, BookSummary

client = TestClient(app)

MOCK_SUMMARY = BookSummary(
    id="abc123",
    title="テスト本",
    authors=["著者A"],
    thumbnail="https://example.com/thumb.jpg",
    published_date="2024-01-01",
    description="概要",
)

MOCK_DETAIL = BookDetail(
    id="abc123",
    title="テスト本",
    authors=["著者A"],
    thumbnail="https://example.com/thumb.jpg",
    published_date="2024-01-01",
    description="概要",
    page_count=300,
    categories=["技術書"],
    publisher="出版社",
    isbn="9784000000000",
)


def test_search_books():
    mock_response = BookSearchResponse(total=1, limit=10, offset=0, items=[MOCK_SUMMARY])
    with patch(
        "app.routers.books.search_books",
        new=AsyncMock(return_value=mock_response),
    ):
        response = client.get("/books/search?q=テスト")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["id"] == "abc123"


def test_search_books_empty_q():
    response = client.get("/books/search?q=")
    assert response.status_code == 422


def test_get_book_detail():
    with patch(
        "app.routers.books.get_book",
        new=AsyncMock(return_value=MOCK_DETAIL),
    ):
        response = client.get("/books/abc123")
    assert response.status_code == 200
    data = response.json()
    assert data["isbn"] == "9784000000000"


def test_get_book_not_found():
    with patch(
        "app.routers.books.get_book",
        new=AsyncMock(return_value=None),
    ):
        response = client.get("/books/nonexistent")
    assert response.status_code == 404
