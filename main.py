from fastapi import FastAPI
from routers import users, books, authors, categories, purchase_requests

app = FastAPI()

# Include routers
app.include_router(users.router, prefix="", tags=["Users"])
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(authors.router, prefix="/authors", tags=["Authors"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(purchase_requests.router, prefix="/purchase_requests", tags=["Purchase Requests"])
