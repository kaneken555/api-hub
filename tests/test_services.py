import pytest

from app.services.google_books import _extract_isbn, _parse_detail, _parse_summary


def test_parse_summary_full():
    item = {
        "id": "abc123",
        "volumeInfo": {
            "title": "テスト本",
            "authors": ["著者A"],
            "imageLinks": {"thumbnail": "https://example.com/thumb.jpg"},
            "publishedDate": "2024-01-01",
            "description": "概要テキスト",
        },
    }
    result = _parse_summary(item)
    assert result.id == "abc123"
    assert result.title == "テスト本"
    assert result.authors == ["著者A"]
    assert result.thumbnail == "https://example.com/thumb.jpg"
    assert result.published_date == "2024-01-01"
    assert result.description == "概要テキスト"


def test_parse_summary_missing_fields():
    item = {"id": "abc123", "volumeInfo": {"title": "タイトルのみ"}}
    result = _parse_summary(item)
    assert result.authors is None
    assert result.thumbnail is None
    assert result.published_date is None
    assert result.description is None


def test_parse_detail_isbn():
    item = {
        "id": "xyz",
        "volumeInfo": {
            "title": "詳細本",
            "industryIdentifiers": [
                {"type": "ISBN_13", "identifier": "9784000000000"},
                {"type": "ISBN_10", "identifier": "4000000000"},
            ],
            "pageCount": 300,
            "categories": ["技術書"],
            "publisher": "出版社",
        },
    }
    result = _parse_detail(item)
    assert result.isbn == "9784000000000"
    assert result.page_count == 300
    assert result.categories == ["技術書"]
    assert result.publisher == "出版社"


def test_extract_isbn_prefers_isbn13():
    identifiers = [
        {"type": "ISBN_10", "identifier": "4000000000"},
        {"type": "ISBN_13", "identifier": "9784000000000"},
    ]
    assert _extract_isbn(identifiers) == "9784000000000"


def test_extract_isbn_fallback_to_isbn10():
    identifiers = [{"type": "ISBN_10", "identifier": "4000000000"}]
    assert _extract_isbn(identifiers) == "4000000000"


def test_extract_isbn_none():
    assert _extract_isbn(None) is None
    assert _extract_isbn([]) is None
