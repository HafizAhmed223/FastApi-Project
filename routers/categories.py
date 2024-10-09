from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth import has_role
from models import Category
from schemas import CategoryCreate, CategoryResponse
from database import get_db
from typing import List, Annotated

router = APIRouter()


@router.post("/", response_model=CategoryResponse)
async def create_category(user_role: Annotated[str, Depends(has_role(["admin"]))],
                          category: CategoryCreate, db: Session = Depends(get_db)):
    existing_category = db.query(Category).filter(Category.name == category.name).first()
    if existing_category:
        return existing_category
    new_category = Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.get("/", response_model=List[CategoryResponse])
async def get_categories(user_role: Annotated[str, Depends(has_role(["admin", "author", "reader"]))],
                         db: Session = Depends(get_db)):
    return db.query(Category).all()
