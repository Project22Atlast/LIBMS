from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime, timedelta

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models
class Book(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    author: str
    isbn: str
    genre: str
    total_copies: int
    available_copies: int
    description: Optional[str] = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)

class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    genre: str
    total_copies: int
    description: Optional[str] = ""

class Member(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    student_id: str
    grade: str
    picture_base64: Optional[str] = ""
    email: Optional[str] = ""
    phone: Optional[str] = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)

class MemberCreate(BaseModel):
    name: str
    student_id: str
    grade: str
    picture_base64: Optional[str] = ""
    email: Optional[str] = ""
    phone: Optional[str] = ""

class Transaction(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    book_id: str
    member_id: str
    checkout_date: datetime = Field(default_factory=datetime.utcnow)
    due_date: datetime
    return_date: Optional[datetime] = None
    status: str = "borrowed"  # borrowed, returned, overdue
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TransactionCreate(BaseModel):
    book_id: str
    member_id: str

class TransactionWithDetails(BaseModel):
    id: str
    book: dict
    member: dict
    checkout_date: datetime
    due_date: datetime
    return_date: Optional[datetime]
    status: str
    days_overdue: Optional[int] = 0

# Book Routes
@api_router.post("/books", response_model=Book)
async def create_book(book: BookCreate):
    book_dict = book.dict()
    book_dict["available_copies"] = book_dict["total_copies"]
    book_obj = Book(**book_dict)
    await db.books.insert_one(book_obj.dict())
    return book_obj

@api_router.get("/books", response_model=List[Book])
async def get_books():
    books = await db.books.find().to_list(1000)
    return [Book(**book) for book in books]

@api_router.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: str):
    book = await db.books.find_one({"id": book_id})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return Book(**book)

@api_router.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: str, book: BookCreate):
    existing_book = await db.books.find_one({"id": book_id})
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book_dict = book.dict()
    # Maintain the same available copies ratio if total copies changed
    if book_dict["total_copies"] != existing_book["total_copies"]:
        borrowed_copies = existing_book["total_copies"] - existing_book["available_copies"]
        book_dict["available_copies"] = max(0, book_dict["total_copies"] - borrowed_copies)
    else:
        book_dict["available_copies"] = existing_book["available_copies"]
    
    await db.books.update_one({"id": book_id}, {"$set": book_dict})
    updated_book = await db.books.find_one({"id": book_id})
    return Book(**updated_book)

@api_router.delete("/books/{book_id}")
async def delete_book(book_id: str):
    # Check if book is borrowed
    borrowed_count = await db.transactions.count_documents({"book_id": book_id, "status": "borrowed"})
    if borrowed_count > 0:
        raise HTTPException(status_code=400, detail="Cannot delete book that is currently borrowed")
    
    result = await db.books.delete_one({"id": book_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}

# Member Routes
@api_router.post("/members", response_model=Member)
async def create_member(member: MemberCreate):
    # Check if student_id already exists
    existing_member = await db.members.find_one({"student_id": member.student_id})
    if existing_member:
        raise HTTPException(status_code=400, detail="Student ID already exists")
    
    member_obj = Member(**member.dict())
    await db.members.insert_one(member_obj.dict())
    return member_obj

@api_router.get("/members", response_model=List[Member])
async def get_members():
    members = await db.members.find().to_list(1000)
    return [Member(**member) for member in members]

@api_router.get("/members/{member_id}", response_model=Member)
async def get_member(member_id: str):
    member = await db.members.find_one({"id": member_id})
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return Member(**member)

@api_router.put("/members/{member_id}", response_model=Member)
async def update_member(member_id: str, member: MemberCreate):
    existing_member = await db.members.find_one({"id": member_id})
    if not existing_member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Check if student_id is being changed and if it conflicts
    if member.student_id != existing_member["student_id"]:
        conflicting_member = await db.members.find_one({"student_id": member.student_id})
        if conflicting_member:
            raise HTTPException(status_code=400, detail="Student ID already exists")
    
    await db.members.update_one({"id": member_id}, {"$set": member.dict()})
    updated_member = await db.members.find_one({"id": member_id})
    return Member(**updated_member)

@api_router.delete("/members/{member_id}")
async def delete_member(member_id: str):
    # Check if member has borrowed books
    borrowed_count = await db.transactions.count_documents({"member_id": member_id, "status": "borrowed"})
    if borrowed_count > 0:
        raise HTTPException(status_code=400, detail="Cannot delete member who has borrowed books")
    
    result = await db.members.delete_one({"id": member_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"message": "Member deleted successfully"}

# Transaction Routes
@api_router.post("/transactions/checkout", response_model=Transaction)
async def checkout_book(transaction: TransactionCreate):
    # Check if book exists and is available
    book = await db.books.find_one({"id": transaction.book_id})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if book["available_copies"] <= 0:
        raise HTTPException(status_code=400, detail="Book not available")
    
    # Check if member exists
    member = await db.members.find_one({"id": transaction.member_id})
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Check if member already has this book
    existing_transaction = await db.transactions.find_one({
        "book_id": transaction.book_id, 
        "member_id": transaction.member_id, 
        "status": "borrowed"
    })
    if existing_transaction:
        raise HTTPException(status_code=400, detail="Member already has this book borrowed")
    
    # Create transaction
    due_date = datetime.utcnow() + timedelta(days=14)  # 14 days borrowing period
    transaction_obj = Transaction(
        book_id=transaction.book_id,
        member_id=transaction.member_id,
        due_date=due_date
    )
    
    await db.transactions.insert_one(transaction_obj.dict())
    
    # Update book available copies
    await db.books.update_one(
        {"id": transaction.book_id}, 
        {"$inc": {"available_copies": -1}}
    )
    
    return transaction_obj

@api_router.post("/transactions/{transaction_id}/return")
async def return_book(transaction_id: str):
    transaction = await db.transactions.find_one({"id": transaction_id})
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    if transaction["status"] != "borrowed":
        raise HTTPException(status_code=400, detail="Book is not currently borrowed")
    
    # Update transaction
    return_date = datetime.utcnow()
    await db.transactions.update_one(
        {"id": transaction_id}, 
        {"$set": {"return_date": return_date, "status": "returned"}}
    )
    
    # Update book available copies
    await db.books.update_one(
        {"id": transaction["book_id"]}, 
        {"$inc": {"available_copies": 1}}
    )
    
    return {"message": "Book returned successfully"}

@api_router.get("/transactions", response_model=List[TransactionWithDetails])
async def get_transactions():
    transactions = await db.transactions.find().sort("created_at", -1).to_list(1000)
    
    result = []
    for transaction in transactions:
        book = await db.books.find_one({"id": transaction["book_id"]})
        member = await db.members.find_one({"id": transaction["member_id"]})
        
        days_overdue = 0
        if transaction["status"] == "borrowed" and transaction["due_date"] < datetime.utcnow():
            days_overdue = (datetime.utcnow() - transaction["due_date"]).days
            # Update status to overdue
            await db.transactions.update_one(
                {"id": transaction["id"]}, 
                {"$set": {"status": "overdue"}}
            )
            transaction["status"] = "overdue"
        
        result.append(TransactionWithDetails(
            id=transaction["id"],
            book=book or {},
            member=member or {},
            checkout_date=transaction["checkout_date"],
            due_date=transaction["due_date"],
            return_date=transaction.get("return_date"),
            status=transaction["status"],
            days_overdue=days_overdue
        ))
    
    return result

@api_router.get("/dashboard/stats")
async def get_dashboard_stats():
    total_books = await db.books.count_documents({})
    total_members = await db.members.count_documents({})
    
    # Calculate total copies and available copies
    books_cursor = db.books.aggregate([
        {
            "$group": {
                "_id": None,
                "total_copies": {"$sum": "$total_copies"},
                "available_copies": {"$sum": "$available_copies"}
            }
        }
    ])
    books_stats = await books_cursor.to_list(1)
    
    total_copies = books_stats[0]["total_copies"] if books_stats else 0
    available_copies = books_stats[0]["available_copies"] if books_stats else 0
    borrowed_books = total_copies - available_copies
    
    overdue_count = await db.transactions.count_documents({
        "status": "borrowed",
        "due_date": {"$lt": datetime.utcnow()}
    })
    
    return {
        "total_books": total_books,
        "total_members": total_members,
        "total_copies": total_copies,
        "borrowed_books": borrowed_books,
        "available_copies": available_copies,
        "overdue_books": overdue_count
    }

# Search Routes
@api_router.get("/search/books")
async def search_books(q: str = "", genre: str = "", available_only: bool = False):
    query = {}
    
    if q:
        query["$or"] = [
            {"title": {"$regex": q, "$options": "i"}},
            {"author": {"$regex": q, "$options": "i"}},
            {"isbn": {"$regex": q, "$options": "i"}}
        ]
    
    if genre:
        query["genre"] = {"$regex": genre, "$options": "i"}
    
    if available_only:
        query["available_copies"] = {"$gt": 0}
    
    books = await db.books.find(query).to_list(1000)
    return [Book(**book) for book in books]

@api_router.get("/search/members")
async def search_members(q: str = "", grade: str = ""):
    query = {}
    
    if q:
        query["$or"] = [
            {"name": {"$regex": q, "$options": "i"}},
            {"student_id": {"$regex": q, "$options": "i"}},
            {"email": {"$regex": q, "$options": "i"}}
        ]
    
    if grade:
        query["grade"] = {"$regex": grade, "$options": "i"}
    
    members = await db.members.find(query).to_list(1000)
    return [Member(**member) for member in members]

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()