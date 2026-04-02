from dotenv import load_dotenv
from fastapi import FastAPI

from app.routers.books import router as books_router

load_dotenv()

app = FastAPI(title="api-hub")

app.include_router(books_router)
