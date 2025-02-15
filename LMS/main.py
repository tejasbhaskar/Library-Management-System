#library management system
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  author TEXT NOT NULL,
                  year INTEGER NOT NULL,
                  available INTEGER DEFAULT 1)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS issued_books (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  book_id INTEGER,
                  issued_to TEXT,
                  FOREIGN KEY (book_id) REFERENCES books (id))''')

conn.commit()

def add_book():
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    year = input("Enter publication year: ")
    cursor.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, year))
    conn.commit()
    print("Book added successfully!")

def remove_book():
    book_id = input("Enter book ID to remove: ")
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    print("Book removed successfully!")

def search_book():
    search_term = input("Enter book title or author to search: ")
    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", (f"%{search_term}%", f"%{search_term}%"))
    books = cursor.fetchall()
    if books:
        for book in books:
            print(book)
    else:
        print("No books found.")

def view_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    if books:
        for book in books:
            print(book)
    else:
        print("No books available.")

def issue_book():
    book_id = input("Enter book ID to issue: ")
    issued_to = input("Enter name of the person: ")
    
    cursor.execute("SELECT available FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    
    if book and book[0] == 1:
        cursor.execute("INSERT INTO issued_books (book_id, issued_to) VALUES (?, ?)", (book_id, issued_to))
        cursor.execute("UPDATE books SET available = 0 WHERE id = ?", (book_id,))
        conn.commit()
        print("Book issued successfully!")
    else:
        print("Book is not available.")

def return_book():
    book_id = input("Enter book ID to return: ")
    cursor.execute("DELETE FROM issued_books WHERE book_id = ?", (book_id,))
    cursor.execute("UPDATE books SET available = 1 WHERE id = ?", (book_id,))
    conn.commit()
    print("Book returned successfully!")

while True:
    print("\nLibrary Management System")
    print("1. Add Book")
    print("2. Remove Book")
    print("3. Search Book")
    print("4. View All Books")
    print("5. Issue Book")
    print("6. Return Book")
    print("7. Exit")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        add_book()
    elif choice == "2":
        remove_book()
    elif choice == "3":
        search_book()
    elif choice == "4":
        view_books()
    elif choice == "5":
        issue_book()
    elif choice == "6":
        return_book()
    elif choice == "7":
        print("Exiting...")
        break
    else:
        print("Invalid choice! Please try again.")
