from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from sqlalchemy import select
from database.models import AdvancedData


router = APIRouter(
    prefix="/advanced",
    tags=["advanced"]
)

@router.get("")
def get_advanced_data(db: Session = Depends(get_db)):
    result = db.execute(select(AdvancedData).limit(10))
    rows = result.scalars().all()
    return rows

@router.get("/{id}")
def get_advanced_book_data(id: int, db: Session = Depends(get_db)):
    book = db.execute(select(AdvancedData).where(AdvancedData.id == id))
    result = book.scalar()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book with id: {id} does not exist")
    return result