from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Book Model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Boolean, default=True)

# Create Database
with app.app_context():
    db.create_all()

# Home Route (View Books)
@app.route("/")
def index():
    books = Book.query.all()
    return render_template("index.html", books=books)

# Add Book Route
@app.route("/add", methods=["POST"])
def add_book():
    title = request.form["title"]
    author = request.form["author"]
    year = request.form["year"]
    new_book = Book(title=title, author=author, year=int(year))
    db.session.add(new_book)
    db.session.commit()
    return redirect(url_for("index"))

# Remove Book Route
@app.route("/delete/<int:id>")
def delete_book(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("index"))

# Issue Book Route
@app.route("/issue/<int:id>")
def issue_book(id):
    book = Book.query.get(id)
    book.available = False
    db.session.commit()
    return redirect(url_for("index"))

# Return Book Route
@app.route("/return/<int:id>")
def return_book(id):
    book = Book.query.get(id)
    book.available = True
    db.session.commit()
    return redirect(url_for("index"))
# search Book Route
@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")
    if query:
        books = Book.query.filter(
            (Book.title.ilike(f"%{query}%")) | (Book.author.ilike(f"%{query}%"))
        ).all()
    else:
        books = Book.query.all()
    return render_template("index.html", books=books)


if __name__ == "__main__":
    app.run(debug=True)
