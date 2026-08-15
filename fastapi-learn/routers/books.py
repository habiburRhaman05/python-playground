from enum import Enum
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# FIX: Import APIRouter with standard casing
router = APIRouter(
    prefix="/books",
    tags=["books"]
)

# FIX: Inherit from str to ensure correct JSON serialization
class BookType(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"

class CreateBookPayload(BaseModel):
    name: str
    price: int
    author: str | None = None  # Example optional field
    type: BookType

    # Strict configuration to forbid outside fields
    model_config = {
        "extra": "forbid"
    }

class CreateBookResponse(BaseModel):
    success: bool
    # FIX: If returning the entire database, this must be a list of payloads
    data: list[CreateBookPayload]

# Mock database array
book_db = []

@router.get("/")
def get_all_books():
    # FIX: Wrap dictionary keys in strings
    return {"books": book_db, "message": "Fetch all books successfully"}

# FIX: Path parameter variable matches function argument

@router.post("/", response_model=CreateBookResponse)
def create_book(book: CreateBookPayload):
    book_db.append(book)
    # FIX: String keys used, Python capitalized boolean 'True' passed
    return {"data": book_db, "success": True}

@router.put("/{book_id}", response_model=CreateBookResponse)
def update_book(book_id: int, book: CreateBookPayload):
    # FIX: Ensure item exists before modifying it in-place
    if 0 <= book_id < len(book_db):
        book_db[book_id] = book
        return {"data": book_db, "success": True}
    
    raise HTTPException(status_code=404, detail="Book index not found to update")

@router.delete("/{book_id}")
def delete_book(book_id: int):
    # FIX: Remove item safely from list by index position
    if 0 <= book_id < len(book_db):
        deleted_item = book_db.pop(book_id)
        return {"message": f"Deleted book: {deleted_item.name}", "success": True}
        
    raise HTTPException(status_code=404, detail="Book index not found to delete")
