from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth import has_role
from models import Author
from schemas import AuthorCreate, AuthorResponse
from database import get_db
from typing import List, Annotated

router = APIRouter()


@router.post("/", response_model=AuthorResponse)
async def create_author(user_role: Annotated[str, Depends(has_role(["admin", "author"]))],
                        author: AuthorCreate, db: Session = Depends(get_db)):
    existing_author = db.query(Author).filter(Author.name == author.name).first()
    if existing_author:
        return existing_author
    new_author = Author(name=author.name)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


@router.get("/", response_model=List[AuthorResponse])
async def get_authors(user_role: Annotated[str, Depends(has_role(["admin", "author", "reader"]))],
                      db: Session = Depends(get_db)):
    return db.query(Author).all()
