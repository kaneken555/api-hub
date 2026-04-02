from pydantic import BaseModel


class BookSummary(BaseModel):
    id: str
    title: str
    authors: list[str] | None
    thumbnail: str | None
    published_date: str | None
    description: str | None


class BookSearchResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[BookSummary]


class BookDetail(BookSummary):
    page_count: int | None
    categories: list[str] | None
    publisher: str | None
    isbn: str | None
