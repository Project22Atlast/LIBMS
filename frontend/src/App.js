import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Book Management Component
const BookManager = ({ onBookAdded }) => {
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    title: "",
    author: "",
    isbn: "",
    genre: "",
    total_copies: 1,
    description: ""
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API}/books`, {
        ...formData,
        total_copies: parseInt(formData.total_copies)
      });
      setFormData({
        title: "",
        author: "",
        isbn: "",
        genre: "",
        total_copies: 1,
        description: ""
      });
      setShowForm(false);
      onBookAdded();
      alert("Book added successfully!");
    } catch (error) {
      alert("Error adding book: " + error.response?.data?.detail || error.message);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold text-gray-800">Book Management</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors"
        >
          {showForm ? "Cancel" : "Add New Book"}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
          <input
            type="text"
            placeholder="Book Title"
            value={formData.title}
            onChange={(e) => setFormData({...formData, title: e.target.value})}
            className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
          <input
            type="text"
            placeholder="Author"
            value={formData.author}
            onChange={(e) => setFormData({...formData, author: e.target.value})}
            className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
          <input
            type="text"
            placeholder="ISBN"
            value={formData.isbn}
            onChange={(e) => setFormData({...formData, isbn: e.target.value})}
            className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
          <input
            type="text"
            placeholder="Genre"
            value={formData.genre}
            onChange={(e) => setFormData({...formData, genre: e.target.value})}
            className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
          <input
            type="number"
            placeholder="Total Copies"
            min="1"
            value={formData.total_copies}
            onChange={(e) => setFormData({...formData, total_copies: e.target.value})}
            className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
          <textarea
            placeholder="Description (optional)"
            value={formData.description}
            onChange={(e) => setFormData({...formData, description: e.target.value})}
            className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 col-span-2"
            rows="2"
          />
          <button
            type="submit"
            className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg transition-colors col-span-2"
          >
            Add Book
          </button>
        </form>
      )}
    </div>
  );
};

// Member Management Component
const MemberManager = ({ onMemberAdded }) => {
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    student_id: "",
    grade: "",
    email: "",
    phone: "",
    picture_base64: ""
  });

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setFormData({...formData, picture_base64: reader.result});
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API}/members`, formData);
      setFormData({
        name: "",
        student_id: "",
        grade: "",
        email: "",
        phone: "",
        picture_base64: ""
      });
      setShowForm(false);
      onMemberAdded();
      alert("Student added successfully!");
    } catch (error) {
      alert("Error adding student: " + error.response?.data?.detail || error.message);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold text-gray-800">Student Management</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded-lg transition-colors"
        >
          {showForm ? "Cancel" : "Add New Student"}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
          <input
            type="text"
            placeholder="Student Name"
            value={formData.name}
            onChange={(e) => setFormData({...formData, name: e.target.value})}
            className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
            required
          />
          <input
            type="text"
            placeholder="Student ID"
            value={formData.student_id}
            onChange={(e) => setFormData({...formData, student_id: e.target.value})}
            className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
            required
          />
          <input
            type="text"
            placeholder="Grade/Class"
            value={formData.grade}
            onChange={(e) => setFormData({...formData, grade: e.target.value})}
            className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
            required
          />
          <input
            type="email"
            placeholder="Email (optional)"
            value={formData.email}
            onChange={(e) => setFormData({...formData, email: e.target.value})}
            className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
          <input
            type="tel"
            placeholder="Phone (optional)"
            value={formData.phone}
            onChange={(e) => setFormData({...formData, phone: e.target.value})}
            className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
          <div className="col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Student Photo
            </label>
            <input
              type="file"
              accept="image/*"
              onChange={handleImageUpload}
              className="border border-gray-300 rounded-lg px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-purple-500"
            />
            {formData.picture_base64 && (
              <img
                src={formData.picture_base64}
                alt="Preview"
                className="mt-2 w-20 h-20 object-cover rounded-full"
              />
            )}
          </div>
          <button
            type="submit"
            className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg transition-colors col-span-2"
          >
            Add Student
          </button>
        </form>
      )}
    </div>
  );
};

// Borrowing Component
const BorrowingManager = ({ books, members, onTransactionUpdate }) => {
  const [selectedBook, setSelectedBook] = useState("");
  const [selectedMember, setSelectedMember] = useState("");
  const [transactions, setTransactions] = useState([]);
  const [bookSearch, setBookSearch] = useState("");
  const [memberSearch, setMemberSearch] = useState("");

  const fetchTransactions = async () => {
    try {
      const response = await axios.get(`${API}/transactions`);
      setTransactions(response.data);
    } catch (error) {
      console.error("Error fetching transactions:", error);
    }
  };

  useEffect(() => {
    fetchTransactions();
  }, []);

  const handleCheckout = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API}/transactions/checkout`, {
        book_id: selectedBook,
        member_id: selectedMember
      });
      setSelectedBook("");
      setSelectedMember("");
      fetchTransactions();
      onTransactionUpdate();
      alert("Book checked out successfully!");
    } catch (error) {
      alert("Error checking out book: " + error.response?.data?.detail || error.message);
    }
  };

  const handleReturn = async (transactionId) => {
    try {
      await axios.post(`${API}/transactions/${transactionId}/return`);
      fetchTransactions();
      onTransactionUpdate();
      alert("Book returned successfully!");
    } catch (error) {
      alert("Error returning book: " + error.response?.data?.detail || error.message);
    }
  };

  const filteredBooks = books.filter(book => 
    book.title.toLowerCase().includes(bookSearch.toLowerCase()) ||
    book.author.toLowerCase().includes(bookSearch.toLowerCase())
  ).filter(book => book.available_copies > 0);

  const filteredMembers = members.filter(member =>
    member.name.toLowerCase().includes(memberSearch.toLowerCase()) ||
    member.student_id.toLowerCase().includes(memberSearch.toLowerCase())
  );

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 className="text-xl font-bold text-gray-800 mb-4">Book Borrowing</h2>
      
      {/* Checkout Form */}
      <form onSubmit={handleCheckout} className="grid grid-cols-2 gap-4 mb-6 p-4 bg-gray-50 rounded-lg">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Select Book</label>
          <input
            type="text"
            placeholder="Search books..."
            value={bookSearch}
            onChange={(e) => setBookSearch(e.target.value)}
            className="border border-gray-300 rounded-lg px-3 py-2 w-full mb-2 focus:outline-none focus:ring-2 focus:ring-green-500"
          />
          <select
            value={selectedBook}
            onChange={(e) => setSelectedBook(e.target.value)}
            className="border border-gray-300 rounded-lg px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-green-500"
            required
          >
            <option value="">Choose a book...</option>
            {filteredBooks.map(book => (
              <option key={book.id} value={book.id}>
                {book.title} by {book.author} (Available: {book.available_copies})
              </option>
            ))}
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Select Student</label>
          <input
            type="text"
            placeholder="Search students..."
            value={memberSearch}
            onChange={(e) => setMemberSearch(e.target.value)}
            className="border border-gray-300 rounded-lg px-3 py-2 w-full mb-2 focus:outline-none focus:ring-2 focus:ring-green-500"
          />
          <select
            value={selectedMember}
            onChange={(e) => setSelectedMember(e.target.value)}
            className="border border-gray-300 rounded-lg px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-green-500"
            required
          >
            <option value="">Choose a student...</option>
            {filteredMembers.map(member => (
              <option key={member.id} value={member.id}>
                {member.name} ({member.student_id}) - Grade {member.grade}
              </option>
            ))}
          </select>
        </div>
        
        <button
          type="submit"
          className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg transition-colors col-span-2"
        >
          Check Out Book
        </button>
      </form>

      {/* Current Borrowings */}
      <div>
        <h3 className="text-lg font-semibold text-gray-800 mb-3">Current Borrowings</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full table-auto">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-2 text-left">Student</th>
                <th className="px-4 py-2 text-left">Book</th>
                <th className="px-4 py-2 text-left">Due Date</th>
                <th className="px-4 py-2 text-left">Status</th>
                <th className="px-4 py-2 text-left">Action</th>
              </tr>
            </thead>
            <tbody>
              {transactions.filter(t => t.status === 'borrowed' || t.status === 'overdue').map(transaction => (
                <tr key={transaction.id} className="border-b">
                  <td className="px-4 py-2">
                    <div className="flex items-center">
                      {transaction.member.picture_base64 && (
                        <img
                          src={transaction.member.picture_base64}
                          alt={transaction.member.name}
                          className="w-8 h-8 rounded-full mr-2 object-cover"
                        />
                      )}
                      <div>
                        <div className="font-medium">{transaction.member.name}</div>
                        <div className="text-sm text-gray-500">{transaction.member.student_id}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-4 py-2">
                    <div className="font-medium">{transaction.book.title}</div>
                    <div className="text-sm text-gray-500">{transaction.book.author}</div>
                  </td>
                  <td className="px-4 py-2">
                    {new Date(transaction.due_date).toLocaleDateString()}
                  </td>
                  <td className="px-4 py-2">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      transaction.status === 'overdue' 
                        ? 'bg-red-100 text-red-800' 
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {transaction.status === 'overdue' 
                        ? `Overdue (${transaction.days_overdue} days)` 
                        : 'Borrowed'}
                    </span>
                  </td>
                  <td className="px-4 py-2">
                    <button
                      onClick={() => handleReturn(transaction.id)}
                      className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded text-sm transition-colors"
                    >
                      Return
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

// Dashboard Component
const Dashboard = ({ stats }) => {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-6">
      <div className="bg-blue-500 text-white p-4 rounded-lg shadow-md">
        <div className="text-2xl font-bold">{stats.total_books}</div>
        <div className="text-sm opacity-90">Total Books</div>
      </div>
      <div className="bg-purple-500 text-white p-4 rounded-lg shadow-md">
        <div className="text-2xl font-bold">{stats.total_members}</div>
        <div className="text-sm opacity-90">Students</div>
      </div>
      <div className="bg-green-500 text-white p-4 rounded-lg shadow-md">
        <div className="text-2xl font-bold">{stats.total_copies}</div>
        <div className="text-sm opacity-90">Total Copies</div>
      </div>
      <div className="bg-yellow-500 text-white p-4 rounded-lg shadow-md">
        <div className="text-2xl font-bold">{stats.borrowed_books}</div>
        <div className="text-sm opacity-90">Borrowed</div>
      </div>
      <div className="bg-teal-500 text-white p-4 rounded-lg shadow-md">
        <div className="text-2xl font-bold">{stats.available_copies}</div>
        <div className="text-sm opacity-90">Available</div>
      </div>
      <div className="bg-red-500 text-white p-4 rounded-lg shadow-md">
        <div className="text-2xl font-bold">{stats.overdue_books}</div>
        <div className="text-sm opacity-90">Overdue</div>
      </div>
    </div>
  );
};

// Main App
function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [books, setBooks] = useState([]);
  const [members, setMembers] = useState([]);
  const [stats, setStats] = useState({});

  const fetchData = async () => {
    try {
      const [booksRes, membersRes, statsRes] = await Promise.all([
        axios.get(`${API}/books`),
        axios.get(`${API}/members`),
        axios.get(`${API}/dashboard/stats`)
      ]);
      setBooks(booksRes.data);
      setMembers(membersRes.data);
      setStats(statsRes.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-800 flex items-center">
              📚 School Library Management System
            </h1>
            <div className="text-sm text-gray-600">
              Welcome to your library dashboard
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-gray-800 text-white">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex space-x-8">
            {[
              { id: 'dashboard', name: 'Dashboard', icon: '📊' },
              { id: 'books', name: 'Books', icon: '📖' },
              { id: 'members', name: 'Students', icon: '👥' },
              { id: 'borrowing', name: 'Borrowing', icon: '📝' }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-3 font-medium transition-colors ${
                  activeTab === tab.id 
                    ? 'border-b-2 border-blue-400 text-blue-400' 
                    : 'hover:text-gray-300'
                }`}
              >
                {tab.icon} {tab.name}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        {activeTab === 'dashboard' && <Dashboard stats={stats} />}
        
        {activeTab === 'books' && (
          <BookManager onBookAdded={fetchData} />
        )}
        
        {activeTab === 'members' && (
          <MemberManager onMemberAdded={fetchData} />
        )}
        
        {activeTab === 'borrowing' && (
          <BorrowingManager 
            books={books} 
            members={members} 
            onTransactionUpdate={fetchData} 
          />
        )}
      </main>
    </div>
  );
}

export default App;