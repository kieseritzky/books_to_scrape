from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.connection import get_db
from sqlalchemy import select
from database.models import BasicData

router = APIRouter(
    prefix = "/basic",
    tags = ["basic"]
)

@router.get("")
def get_basic_data(db: Session = Depends(get_db)):
    result = db.execute(select(BasicData).limit(10))
    rows = result.scalars().all()
    return rows


@router.get("/{id}")
def get_basic_book_data(id: int, db: Session = Depends(get_db)):
    book = db.execute(select(BasicData).where(BasicData.id == id))
    result = book.scalar()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book with id: {id} does not exist")
    return result