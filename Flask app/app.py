from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ✅ Configure MySQL Database Connection
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:NewPassword123!@localhost/library_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# ✅ Book Model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Boolean, default=True)

# ✅ Create Database Tables
with app.app_context():
    db.create_all()
    print("✅ Database tables created successfully.")

# ✅ Home Route (View Books)
@app.route("/")
def index():
    books = Book.query.all()
    print("📚 Fetching books from database...")
    
    # Debugging: Print book details
    for book in books:
        print(f"📖 {book.id} - {book.title} by {book.author} ({book.year}), Available: {book.available}")

    return render_template("index.html", books=books)

# ✅ Add Book Route
@app.route("/add", methods=["POST"])
def add_book():
    try:
        title = request.form["title"]
        author = request.form["author"]
        year = request.form["year"]

        # Debugging print statements
        print("📥 Received Data:", title, author, year)

        new_book = Book(title=title, author=author, year=int(year))
        db.session.add(new_book)
        db.session.commit()

        print("✅ Book added successfully!")  # Debugging
    except Exception as e:
        print("❌ Error adding book:", str(e))  # Debugging
        db.session.rollback()  # Rollback in case of error

    return redirect(url_for("index"))

# ✅ Remove Book Route
@app.route("/delete/<int:id>")
def delete_book(id):
    book = Book.query.get(id)
    if book:
        db.session.delete(book)
        db.session.commit()
        print(f"✅ Book Deleted: {book.id} - {book.title}")
    return redirect(url_for("index"))

# ✅ Issue Book Route
@app.route("/issue/<int:id>")
def issue_book(id):
    book = Book.query.get(id)
    if book and book.available:
        book.available = False
        db.session.commit()
        print(f"📕 Book Issued: {book.id} - {book.title}")
    return redirect(url_for("index"))

# ✅ Return Book Route
@app.route("/return/<int:id>")
def return_book(id):
    book = Book.query.get(id)
    if book and not book.available:
        book.available = True
        db.session.commit()
        print(f"📗 Book Returned: {book.id} - {book.title}")
    return redirect(url_for("index"))

# ✅ Search Book Route
@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query", "").strip()
    books = Book.query.filter(
        (Book.title.ilike(f"%{query}%")) | (Book.author.ilike(f"%{query}%"))
    ).all()
    print(f"🔍 Searching for: {query} - {len(books)} results found.")
    return render_template("index.html", books=books)

if __name__ == "__main__":
    app.run(debug=True)
