from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float


app = Flask(__name__)

##CREATE DATABASE
class Base(DeclarativeBase):
    pass

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
# Create the extension
db = SQLAlchemy(model_class=Base)
# Initialise the app with the extension
db.init_app(app)


##CREATE TABLE
class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(nullable=False)
    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'

# Create table schema in the database. Requires application context.
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    ##READ ALL RECORDS
    # Construct a query to select from the database. Returns the rows in the database
    result = db.session.execute(db.select(Book).order_by(Book.title)) # Grab fresh data from the database every time, so reloading the page doesn't erase anything.
    all_books = result.scalars().all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        ## CREATE RECORD
        new_book = Book(
            title = request.form["title"],
            author = request.form["author"],
            rating = float(request.form["rating"]),
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/edit/<int:book_id>", methods=['GET', 'POST'])
def edit(book_id):
    book_to_update = db.get_or_404(Book, book_id)
    ## UPDATE RECORD
    if request.method == "POST":
        new_rating = float(request.form["rating"]) # フォームから新しい評価をもらって
        book_to_update.rating = new_rating # その評価を本の情報に上書き！
        db.session.commit() # データベースに保存！！
        return redirect(url_for('home'))
    return render_template("edit.html", book=book_to_update)


@app.route("/delete/<int:book_id>", methods=['GET', 'POST'])
def delete(book_id):
    book_to_delete = db.get_or_404(Book, book_id)
    ## DELETE RECORD
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

