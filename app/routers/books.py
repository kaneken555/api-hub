from fastapi import APIRouter, HTTPException, Query

from app.schemas.book import BookDetail, BookSearchResponse
from app.services.google_books import get_book, search_books

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/search", response_model=BookSearchResponse)
async def search(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=10, ge=1, le=40),
    offset: int = Query(default=0, ge=0),
) -> BookSearchResponse:
    return await search_books(q=q, limit=limit, offset=offset)


@router.get("/{book_id}", response_model=BookDetail)
async def get_book_detail(book_id: str) -> BookDetail:
    book = await get_book(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="書籍が見つかりませんでした")
    return book
