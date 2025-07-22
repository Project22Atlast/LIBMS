#!/usr/bin/env python3
"""
Comprehensive Backend Testing for Library Management System
Tests all high-priority backend functionality with realistic data
"""

import requests
import json
import base64
from datetime import datetime, timedelta
import time

# Get backend URL from environment
BACKEND_URL = "https://8b7e9b12-41dd-49d1-aad1-c9bae2bb635e.preview.emergentagent.com/api"

class LibraryBackendTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.session = requests.Session()
        self.created_books = []
        self.created_members = []
        self.created_transactions = []
        
    def log(self, message):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        
    def test_connection(self):
        """Test basic connectivity to the backend"""
        self.log("Testing backend connectivity...")
        try:
            response = self.session.get(f"{self.base_url}/books")
            if response.status_code == 200:
                self.log("✅ Backend connection successful")
                return True
            else:
                self.log(f"❌ Backend connection failed: {response.status_code}")
                return False
        except Exception as e:
            self.log(f"❌ Backend connection error: {str(e)}")
            return False
    
    def create_sample_base64_image(self):
        """Create a small base64 encoded image for testing"""
        # This is a tiny 1x1 pixel PNG image in base64
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    
    def test_book_crud_operations(self):
        """Test Book CRUD Operations"""
        self.log("\n=== Testing Book CRUD Operations ===")
        
        # Test 1: Create Books
        self.log("Testing book creation...")
        books_to_create = [
            {
                "title": "To Kill a Mockingbird",
                "author": "Harper Lee",
                "isbn": "978-0-06-112008-4",
                "genre": "Fiction",
                "total_copies": 5,
                "description": "A classic American novel about racial injustice"
            },
            {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald", 
                "isbn": "978-0-7432-7356-5",
                "genre": "Fiction",
                "total_copies": 3,
                "description": "A story of decadence and excess in the Jazz Age"
            },
            {
                "title": "1984",
                "author": "George Orwell",
                "isbn": "978-0-452-28423-4", 
                "genre": "Dystopian Fiction",
                "total_copies": 4,
                "description": "A dystopian social science fiction novel"
            }
        ]
        
        for book_data in books_to_create:
            try:
                response = self.session.post(f"{self.base_url}/books", json=book_data)
                if response.status_code == 200:
                    book = response.json()
                    self.created_books.append(book)
                    self.log(f"✅ Created book: {book['title']} (ID: {book['id']})")
                    
                    # Verify available_copies equals total_copies
                    if book['available_copies'] == book['total_copies']:
                        self.log(f"✅ Available copies correctly set to {book['available_copies']}")
                    else:
                        self.log(f"❌ Available copies mismatch: {book['available_copies']} != {book['total_copies']}")
                else:
                    self.log(f"❌ Failed to create book {book_data['title']}: {response.status_code} - {response.text}")
            except Exception as e:
                self.log(f"❌ Error creating book {book_data['title']}: {str(e)}")
        
        # Test 2: Get All Books
        self.log("\nTesting get all books...")
        try:
            response = self.session.get(f"{self.base_url}/books")
            if response.status_code == 200:
                books = response.json()
                self.log(f"✅ Retrieved {len(books)} books")
                if len(books) >= len(self.created_books):
                    self.log("✅ All created books are retrievable")
                else:
                    self.log("❌ Some created books are missing")
            else:
                self.log(f"❌ Failed to get books: {response.status_code}")
        except Exception as e:
            self.log(f"❌ Error getting books: {str(e)}")
        
        # Test 3: Get Single Book
        if self.created_books:
            book_id = self.created_books[0]['id']
            self.log(f"\nTesting get single book (ID: {book_id})...")
            try:
                response = self.session.get(f"{self.base_url}/books/{book_id}")
                if response.status_code == 200:
                    book = response.json()
                    self.log(f"✅ Retrieved book: {book['title']}")
                else:
                    self.log(f"❌ Failed to get book: {response.status_code}")
            except Exception as e:
                self.log(f"❌ Error getting book: {str(e)}")
        
        # Test 4: Update Book
        if self.created_books:
            book_id = self.created_books[0]['id']
            self.log(f"\nTesting book update (ID: {book_id})...")
            update_data = {
                "title": "To Kill a Mockingbird (Updated Edition)",
                "author": "Harper Lee",
                "isbn": "978-0-06-112008-4",
                "genre": "Classic Fiction",
                "total_copies": 6,
                "description": "Updated description - A timeless classic about moral courage"
            }
            try:
                response = self.session.put(f"{self.base_url}/books/{book_id}", json=update_data)
                if response.status_code == 200:
                    updated_book = response.json()
                    self.log(f"✅ Updated book: {updated_book['title']}")
                    self.log(f"✅ Total copies updated to: {updated_book['total_copies']}")
                else:
                    self.log(f"❌ Failed to update book: {response.status_code} - {response.text}")
            except Exception as e:
                self.log(f"❌ Error updating book: {str(e)}")
        
        return len(self.created_books) > 0
    
    def test_member_management_with_pictures(self):
        """Test Member/Student Management with Picture Upload"""
        self.log("\n=== Testing Member/Student Management with Picture Upload ===")
        
        # Test 1: Create Members with Pictures
        self.log("Testing member creation with base64 images...")
        sample_image = self.create_sample_base64_image()
        
        members_to_create = [
            {
                "name": "Emma Johnson",
                "student_id": "STU2024001",
                "grade": "10th Grade",
                "picture_base64": sample_image,
                "email": "emma.johnson@school.edu",
                "phone": "(555) 123-4567"
            },
            {
                "name": "Michael Chen",
                "student_id": "STU2024002", 
                "grade": "11th Grade",
                "picture_base64": sample_image,
                "email": "michael.chen@school.edu",
                "phone": "(555) 234-5678"
            },
            {
                "name": "Sarah Williams",
                "student_id": "STU2024003",
                "grade": "9th Grade", 
                "picture_base64": sample_image,
                "email": "sarah.williams@school.edu",
                "phone": "(555) 345-6789"
            }
        ]
        
        for member_data in members_to_create:
            try:
                response = self.session.post(f"{self.base_url}/members", json=member_data)
                if response.status_code == 200:
                    member = response.json()
                    self.created_members.append(member)
                    self.log(f"✅ Created member: {member['name']} (ID: {member['student_id']})")
                    
                    # Verify picture was stored
                    if member.get('picture_base64'):
                        self.log(f"✅ Picture successfully stored for {member['name']}")
                    else:
                        self.log(f"⚠️ Picture not stored for {member['name']}")
                else:
                    self.log(f"❌ Failed to create member {member_data['name']}: {response.status_code} - {response.text}")
            except Exception as e:
                self.log(f"❌ Error creating member {member_data['name']}: {str(e)}")
        
        # Test 2: Test Duplicate Student ID Prevention
        self.log("\nTesting duplicate student ID prevention...")
        if self.created_members:
            duplicate_member = {
                "name": "John Duplicate",
                "student_id": self.created_members[0]['student_id'],  # Use existing student ID
                "grade": "12th Grade",
                "picture_base64": sample_image
            }
            try:
                response = self.session.post(f"{self.base_url}/members", json=duplicate_member)
                if response.status_code == 400:
                    self.log("✅ Duplicate student ID correctly rejected")
                else:
                    self.log(f"❌ Duplicate student ID not rejected: {response.status_code}")
            except Exception as e:
                self.log(f"❌ Error testing duplicate student ID: {str(e)}")
        
        # Test 3: Get All Members
        self.log("\nTesting get all members...")
        try:
            response = self.session.get(f"{self.base_url}/members")
            if response.status_code == 200:
                members = response.json()
                self.log(f"✅ Retrieved {len(members)} members")
                
                # Verify pictures are included
                members_with_pictures = [m for m in members if m.get('picture_base64')]
                self.log(f"✅ {len(members_with_pictures)} members have pictures stored")
            else:
                self.log(f"❌ Failed to get members: {response.status_code}")
        except Exception as e:
            self.log(f"❌ Error getting members: {str(e)}")
        
        # Test 4: Update Member
        if self.created_members:
            member_id = self.created_members[0]['id']
            self.log(f"\nTesting member update (ID: {member_id})...")
            update_data = {
                "name": "Emma Johnson-Smith",
                "student_id": self.created_members[0]['student_id'],
                "grade": "10th Grade",
                "picture_base64": sample_image,
                "email": "emma.johnsonsmith@school.edu",
                "phone": "(555) 123-4567"
            }
            try:
                response = self.session.put(f"{self.base_url}/members/{member_id}", json=update_data)
                if response.status_code == 200:
                    updated_member = response.json()
                    self.log(f"✅ Updated member: {updated_member['name']}")
                else:
                    self.log(f"❌ Failed to update member: {response.status_code} - {response.text}")
            except Exception as e:
                self.log(f"❌ Error updating member: {str(e)}")
        
        return len(self.created_members) > 0
    
    def test_book_borrowing_checkout_system(self):
        """Test Book Borrowing/Checkout System"""
        self.log("\n=== Testing Book Borrowing/Checkout System ===")
        
        if not self.created_books or not self.created_members:
            self.log("❌ Cannot test checkout - no books or members available")
            return False
        
        # Test 1: Valid Checkout
        self.log("Testing valid book checkout...")
        checkout_data = {
            "book_id": self.created_books[0]['id'],
            "member_id": self.created_members[0]['id']
        }
        
        try:
            response = self.session.post(f"{self.base_url}/transactions/checkout", json=checkout_data)
            if response.status_code == 200:
                transaction = response.json()
                self.created_transactions.append(transaction)
                self.log(f"✅ Book checked out successfully (Transaction ID: {transaction['id']})")
                
                # Verify due date is 14 days from now
                due_date = datetime.fromisoformat(transaction['due_date'].replace('Z', '+00:00'))
                expected_due = datetime.utcnow() + timedelta(days=14)
                days_diff = abs((due_date - expected_due).days)
                if days_diff <= 1:  # Allow 1 day tolerance
                    self.log("✅ Due date correctly set to 14 days")
                else:
                    self.log(f"❌ Due date incorrect: {days_diff} days difference")
                
                # Verify book availability decreased
                book_response = self.session.get(f"{self.base_url}/books/{self.created_books[0]['id']}")
                if book_response.status_code == 200:
                    updated_book = book_response.json()
                    if updated_book['available_copies'] == self.created_books[0]['available_copies'] - 1:
                        self.log("✅ Book available copies correctly decreased")
                    else:
                        self.log(f"❌ Available copies not updated correctly")
            else:
                self.log(f"❌ Failed to checkout book: {response.status_code} - {response.text}")
        except Exception as e:
            self.log(f"❌ Error during checkout: {str(e)}")
        
        # Test 2: Duplicate Borrowing Prevention
        self.log("\nTesting duplicate borrowing prevention...")
        try:
            response = self.session.post(f"{self.base_url}/transactions/checkout", json=checkout_data)
            if response.status_code == 400:
                self.log("✅ Duplicate borrowing correctly prevented")
            else:
                self.log(f"❌ Duplicate borrowing not prevented: {response.status_code}")
        except Exception as e:
            self.log(f"❌ Error testing duplicate borrowing: {str(e)}")
        
        # Test 3: Checkout Another Book to Different Member
        if len(self.created_books) > 1 and len(self.created_members) > 1:
            self.log("\nTesting checkout to different member...")
            checkout_data2 = {
                "book_id": self.created_books[1]['id'],
                "member_id": self.created_members[1]['id']
            }
            try:
                response = self.session.post(f"{self.base_url}/transactions/checkout", json=checkout_data2)
                if response.status_code == 200:
                    transaction = response.json()
                    self.created_transactions.append(transaction)
                    self.log(f"✅ Second book checked out successfully")
                else:
                    self.log(f"❌ Failed to checkout second book: {response.status_code}")
            except Exception as e:
                self.log(f"❌ Error checking out second book: {str(e)}")
        
        # Test 4: Try to checkout unavailable book (exhaust all copies)
        if self.created_books:
            book_id = self.created_books[0]['id']
            member_ids = [m['id'] for m in self.created_members[1:]]  # Skip first member who already borrowed
            
            self.log(f"\nTesting availability checks by exhausting copies...")
            # Get current book info
            book_response = self.session.get(f"{self.base_url}/books/{book_id}")
            if book_response.status_code == 200:
                book = book_response.json()
                available = book['available_copies']
                
                # Try to checkout remaining copies
                for i, member_id in enumerate(member_ids[:available]):
                    checkout_data = {"book_id": book_id, "member_id": member_id}
                    response = self.session.post(f"{self.base_url}/transactions/checkout", json=checkout_data)
                    if response.status_code == 200:
                        self.created_transactions.append(response.json())
                        self.log(f"✅ Checkout {i+1} successful")
                    
                # Now try one more checkout - should fail
                if len(member_ids) > available:
                    checkout_data = {"book_id": book_id, "member_id": member_ids[available]}
                    response = self.session.post(f"{self.base_url}/transactions/checkout", json=checkout_data)
                    if response.status_code == 400:
                        self.log("✅ Unavailable book checkout correctly rejected")
                    else:
                        self.log(f"❌ Unavailable book checkout not rejected: {response.status_code}")
        
        return len(self.created_transactions) > 0
    
    def test_book_return_system(self):
        """Test Book Return System"""
        self.log("\n=== Testing Book Return System ===")
        
        if not self.created_transactions:
            self.log("❌ Cannot test returns - no transactions available")
            return False
        
        # Test 1: Valid Return
        transaction_id = self.created_transactions[0]['id']
        book_id = self.created_transactions[0]['book_id']
        
        self.log(f"Testing book return (Transaction ID: {transaction_id})...")
        
        # Get book info before return
        book_response = self.session.get(f"{self.base_url}/books/{book_id}")
        if book_response.status_code == 200:
            book_before = book_response.json()
            available_before = book_before['available_copies']
            
            try:
                response = self.session.post(f"{self.base_url}/transactions/{transaction_id}/return")
                if response.status_code == 200:
                    self.log("✅ Book returned successfully")
                    
                    # Verify book availability increased
                    book_response_after = self.session.get(f"{self.base_url}/books/{book_id}")
                    if book_response_after.status_code == 200:
                        book_after = book_response_after.json()
                        if book_after['available_copies'] == available_before + 1:
                            self.log("✅ Book available copies correctly increased")
                        else:
                            self.log(f"❌ Available copies not updated: {book_after['available_copies']} vs expected {available_before + 1}")
                    
                    # Verify transaction status updated
                    transactions_response = self.session.get(f"{self.base_url}/transactions")
                    if transactions_response.status_code == 200:
                        transactions = transactions_response.json()
                        returned_transaction = next((t for t in transactions if t['id'] == transaction_id), None)
                        if returned_transaction and returned_transaction['status'] == 'returned':
                            self.log("✅ Transaction status correctly updated to 'returned'")
                        else:
                            self.log("❌ Transaction status not updated correctly")
                else:
                    self.log(f"❌ Failed to return book: {response.status_code} - {response.text}")
            except Exception as e:
                self.log(f"❌ Error during return: {str(e)}")
        
        # Test 2: Try to return already returned book
        self.log("\nTesting duplicate return prevention...")
        try:
            response = self.session.post(f"{self.base_url}/transactions/{transaction_id}/return")
            if response.status_code == 400:
                self.log("✅ Duplicate return correctly prevented")
            else:
                self.log(f"❌ Duplicate return not prevented: {response.status_code}")
        except Exception as e:
            self.log(f"❌ Error testing duplicate return: {str(e)}")
        
        return True
    
    def test_search_and_filter_functionality(self):
        """Test Search and Filter Functionality"""
        self.log("\n=== Testing Search and Filter Functionality ===")
        
        # Test 1: Book Search by Title
        self.log("Testing book search by title...")
        try:
            response = self.session.get(f"{self.base_url}/search/books?q=Mockingbird")
            if response.status_code == 200:
                books = response.json()
                if any("Mockingbird" in book['title'] for book in books):
                    self.log("✅ Book search by title working")
                else:
                    self.log("❌ Book search by title not finding expected results")
            else:
                self.log(f"❌ Book search failed: {response.status_code}")
        except Exception as e:
            self.log(f"❌ Error in book search: {str(e)}")
        
        # Test 2: Book Search by Author
        self.log("Testing book search by author...")
        try:
            response = self.session.get(f"{self.base_url}/search/books?q=Harper")
            if response.status_code == 200:
                books = response.json()
                if any("Harper" in book['author'] for book in books):
                    self.log("✅ Book search by author working")
                else:
                    self.log("❌ Book search by author not finding expected results")
            else:
                self.log(f"❌ Book search by author failed: {response.status_code}")
        except Exception as e:
            self.log(f"❌ Error in book search by author: {str(e)}")
        
        # Test 3: Book Search by ISBN
        self.log("Testing book search by ISBN...")
        try:
            response = self.session.get(f"{self.base_url}/search/books?q=978-0-06-112008-4")
            if response.status_code == 200:
                books = response.json()
                if any("978-0-06-112008-4" in book['isbn'] for book in books):
                    self.log("✅ Book search by ISBN working")
                else:
                    self.log("❌ Book search by ISBN not finding expected results")
            else:
                self.log(f"❌ Book search by ISBN failed: {response.status_code}")
        except Exception as e:
            self.log(f"❌ Error in book search by ISBN: {str(e)}")
        
        # Test 4: Book Filter by Genre
        self.log("Testing book filter by genre...")
        try:
            response = self.session.get(f"{self.base_url}/search/books?genre=Fiction")
            if response.status_code == 200:
                books = response.json()
                if all("Fiction" in book['genre'] for book in books if books):
                    self.log("✅ Book filter by genre working")
                else:
                    self.log("❌ Book filter by genre not working correctly")
            else:
                self.log(f"❌ Book filter by genre failed: {response.status_code}")
        except Exception as e:
            self.log(f"❌ Error in book filter by genre: {str(e)}")
        
        # Test 5: Book Filter by Availability
        self.log("Testing book filter by availability...")
        try:
            response = self.session.get(f"{self.base_url}/search/books?available_only=true")
            if response.status_code == 200:
                books = response.json()
                if all(book['available_copies'] > 0 for book in books):
                    self.log("✅ Book filter by availability working")
                else:
                    self.log("❌ Book filter by availability not working correctly")
            else:
                self.log(f"❌ Book filter by availability failed: {response.status_code}")
        except Exception as e:
            self.log(f"❌ Error in book filter by availability: {str(e)}")
        
        # Test 6: Member Search by Name
        self.log("Testing member search by name...")
        try:
            response = self.session.get(f"{self.base_url}/search/members?q=Emma")
            if response.status_code == 200:
                members = response.json()
                if any("Emma" in member['name'] for member in members):
                    self.log("✅ Member search by name working")
                else:
                    self.log("❌ Member search by name not finding expected results")
            else:
                self.log(f"❌ Member search by name failed: {response.status_code}")
        except Exception as e:
            self.log(f"❌ Error in member search by name: {str(e)}")
        
        # Test 7: Member Search by Student ID
        self.log("Testing member search by student ID...")
        try:
            response = self.session.get(f"{self.base_url}/search/members?q=STU2024001")
            if response.status_code == 200:
                members = response.json()
                if any("STU2024001" in member['student_id'] for member in members):
                    self.log("✅ Member search by student ID working")
                else:
                    self.log("❌ Member search by student ID not finding expected results")
            else:
                self.log(f"❌ Member search by student ID failed: {response.status_code}")
        except Exception as e:
            self.log(f"❌ Error in member search by student ID: {str(e)}")
        
        # Test 8: Member Filter by Grade
        self.log("Testing member filter by grade...")
        try:
            response = self.session.get(f"{self.base_url}/search/members?grade=10th")
            if response.status_code == 200:
                members = response.json()
                if all("10th" in member['grade'] for member in members if members):
                    self.log("✅ Member filter by grade working")
                else:
                    self.log("❌ Member filter by grade not working correctly")
            else:
                self.log(f"❌ Member filter by grade failed: {response.status_code}")
        except Exception as e:
            self.log(f"❌ Error in member filter by grade: {str(e)}")
        
        return True
    
    def test_dashboard_statistics(self):
        """Test Dashboard Statistics"""
        self.log("\n=== Testing Dashboard Statistics ===")
        
        try:
            response = self.session.get(f"{self.base_url}/dashboard/stats")
            if response.status_code == 200:
                stats = response.json()
                self.log("✅ Dashboard stats endpoint accessible")
                
                # Verify expected fields are present
                expected_fields = ['total_books', 'total_members', 'total_copies', 'borrowed_books', 'available_copies', 'overdue_books']
                missing_fields = [field for field in expected_fields if field not in stats]
                
                if not missing_fields:
                    self.log("✅ All expected statistics fields present")
                    
                    # Log the actual statistics
                    self.log(f"📊 Statistics Summary:")
                    self.log(f"   - Total Books: {stats['total_books']}")
                    self.log(f"   - Total Members: {stats['total_members']}")
                    self.log(f"   - Total Copies: {stats['total_copies']}")
                    self.log(f"   - Borrowed Books: {stats['borrowed_books']}")
                    self.log(f"   - Available Copies: {stats['available_copies']}")
                    self.log(f"   - Overdue Books: {stats['overdue_books']}")
                    
                    # Verify data consistency
                    if stats['total_copies'] == stats['borrowed_books'] + stats['available_copies']:
                        self.log("✅ Book copy counts are consistent")
                    else:
                        self.log("❌ Book copy counts are inconsistent")
                    
                    # Verify reasonable values
                    if (stats['total_books'] >= 0 and stats['total_members'] >= 0 and 
                        stats['total_copies'] >= 0 and stats['borrowed_books'] >= 0 and
                        stats['available_copies'] >= 0 and stats['overdue_books'] >= 0):
                        self.log("✅ All statistics have reasonable values")
                    else:
                        self.log("❌ Some statistics have unreasonable values")
                        
                else:
                    self.log(f"❌ Missing statistics fields: {missing_fields}")
                    
            else:
                self.log(f"❌ Dashboard stats failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            self.log(f"❌ Error getting dashboard stats: {str(e)}")
            return False
        
        return True
    
    def test_get_transactions(self):
        """Test getting transactions with details"""
        self.log("\n=== Testing Transaction Retrieval ===")
        
        try:
            response = self.session.get(f"{self.base_url}/transactions")
            if response.status_code == 200:
                transactions = response.json()
                self.log(f"✅ Retrieved {len(transactions)} transactions")
                
                if transactions:
                    # Verify transaction structure
                    transaction = transactions[0]
                    expected_fields = ['id', 'book', 'member', 'checkout_date', 'due_date', 'status']
                    missing_fields = [field for field in expected_fields if field not in transaction]
                    
                    if not missing_fields:
                        self.log("✅ Transaction structure is correct")
                        
                        # Verify book and member details are populated
                        if transaction['book'] and transaction['member']:
                            self.log("✅ Transaction includes book and member details")
                        else:
                            self.log("❌ Transaction missing book or member details")
                    else:
                        self.log(f"❌ Transaction missing fields: {missing_fields}")
                        
            else:
                self.log(f"❌ Failed to get transactions: {response.status_code}")
                return False
        except Exception as e:
            self.log(f"❌ Error getting transactions: {str(e)}")
            return False
        
        return True
    
    def run_all_tests(self):
        """Run all backend tests"""
        self.log("🚀 Starting Comprehensive Backend Testing for Library Management System")
        self.log("=" * 80)
        
        # Test connection first
        if not self.test_connection():
            self.log("❌ Cannot proceed - backend not accessible")
            return False
        
        # Run all tests in order
        test_results = {
            "Book CRUD Operations": self.test_book_crud_operations(),
            "Member/Student Management with Picture Upload": self.test_member_management_with_pictures(),
            "Book Borrowing/Checkout System": self.test_book_borrowing_checkout_system(),
            "Book Return System": self.test_book_return_system(),
            "Search and Filter Functionality": self.test_search_and_filter_functionality(),
            "Dashboard Statistics": self.test_dashboard_statistics(),
            "Transaction Retrieval": self.test_get_transactions()
        }
        
        # Summary
        self.log("\n" + "=" * 80)
        self.log("🏁 TESTING SUMMARY")
        self.log("=" * 80)
        
        passed = 0
        total = len(test_results)
        
        for test_name, result in test_results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            self.log(f"{status}: {test_name}")
            if result:
                passed += 1
        
        self.log(f"\nOverall Result: {passed}/{total} tests passed")
        
        if passed == total:
            self.log("🎉 All backend tests PASSED! The library management system is working correctly.")
        else:
            self.log(f"⚠️ {total - passed} test(s) failed. Please review the issues above.")
        
        return test_results

if __name__ == "__main__":
    tester = LibraryBackendTester()
    results = tester.run_all_tests()