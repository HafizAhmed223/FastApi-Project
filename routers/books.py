from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth import has_role
from database import get_db
from models import Book, Author, Category
from schemas import BookCreate, BookResponse, AuthorResponse, CategoryResponse
from typing import List, Annotated

router = APIRouter()


@router.post("/", response_model=BookResponse)
async def create_book(user_role: Annotated[str, Depends(has_role(["admin", "author"]))],
                      book: BookCreate, db: Session = Depends(get_db)):
    # Handle author
    if book.author_name:
        author = db.query(Author).filter(Author.name == book.author_name).first()
        if not author:
            author = Author(name=book.author_name)
            db.add(author)
            db.commit()
            db.refresh(author)
        author_id = author.id
    else:
        author_id = book.author_id

    # Handle category
    if book.category_name:
        category = db.query(Category).filter(Category.name == book.category_name).first()
        if not category:
            category = Category(name=book.category_name)
            db.add(category)
            db.commit()
            db.refresh(category)
        category_id = category.id
    else:
        category_id = book.category_id

    new_book = Book(title=book.title, content=book.content, author_id=author_id, category_id=category_id)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    author = db.query(Author).filter(Author.id == new_book.author_id).first()
    category = db.query(Category).filter(Category.id == new_book.category_id).first()

    return BookResponse(
        id=new_book.id,
        title=new_book.title,
        content=new_book.content,
        author=AuthorResponse(id=author.id, name=author.name),
        category=CategoryResponse(id=category.id, name=category.name)
    )


@router.get("/", response_model=List[BookResponse])
async def get_books(user_role: Annotated[str, Depends(has_role(["admin", "author", "reader"]))],
                    db: Session = Depends(get_db)):
    return db.query(Book).all()
