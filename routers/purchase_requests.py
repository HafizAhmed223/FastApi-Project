from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Book, PurchaseRequests
from schemas import PurchaseRequestCreate, PurchaseRequestResponse
from typing import List, Annotated
from auth import has_role

router = APIRouter()


@router.post("/", response_model=PurchaseRequestResponse)
async def buy_book(user_role: Annotated[str, Depends(has_role(["admin", "reader"]))],
                   request: PurchaseRequestCreate, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == request.book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    new_purchase_request = PurchaseRequests(book_id=request.book_id, reader_name=request.reader_name,
                                            payment_details=request.payment_details)
    db.add(new_purchase_request)
    db.commit()
    db.refresh(new_purchase_request)
    return new_purchase_request


@router.get("/", response_model=List[PurchaseRequestResponse])
async def get_purchase_requests(user_role: Annotated[str, Depends(has_role(["admin"]))], db: Session = Depends(get_db)):
    return db.query(PurchaseRequests).all()


@router.put("/purchase_requests/{purchase_request_id}/{status}")
def update_purchase_request(user_role: Annotated[str, Depends(has_role(["admin"]))],
                            purchase_request_id: int, status: str,
                            db: Session = Depends(get_db)):
    db_purchase_request = db.query(PurchaseRequests).filter(PurchaseRequests.id == purchase_request_id).first()
    if db_purchase_request is None:
        raise HTTPException(status_code=404, detail="Purchase request not found")
    db_purchase_request.status = status
    db.commit()
    db.refresh(db_purchase_request)
    # return db_request
    return {"message": f"Purchase request {purchase_request_id} updated successfully with status {status}"}
