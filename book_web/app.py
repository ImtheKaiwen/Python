from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    year = db.Column(db.Integer, nullable=True)


def init_db():
    db.create_all()
    if not Book.query.first():
        sample_books = [
            Book(title="Savaş ve Barış", author="Lev Tolstoy", category="Roman", year=1869),
            Book(title="Suç ve Ceza", author="Fyodor Dostoyevski", category="Roman", year=1866),
            Book(title="1984", author="George Orwell", category="Distopya", year=1949),
            Book(title="Kürk Mantolu Madonna", author="Sabahattin Ali", category="Roman", year=1943),
            Book(title="Yabancı", author="Albert Camus", category="Felsefi Roman", year=1942),
            Book(title="Şeker Portakalı", author="Jose Mauro de Vasconcelos", category="Roman", year=1968),
            Book(title="Fareler ve İnsanlar", author="John Steinbeck", category="Roman", year=1937),
            Book(title="Cesur Yeni Dünya", author="Aldous Huxley", category="Distopya", year=1932),
            Book(title="Simyacı", author="Paulo Coelho", category="Roman", year=1988),
            Book(title="Uçurtma Avcısı", author="Khaled Hosseini", category="Roman", year=2003),
        ]
        db.session.bulk_save_objects(sample_books)
        db.session.commit()

@app.route('/')
def index():
    query = request.args.get('query')
    category = request.args.get('category')
    
    
    books = Book.query
    if query:
        books = books.filter(Book.title.contains(query) | Book.author.contains(query))
    if category:
        books = books.filter_by(category=category)
    
    books = books.all()
    return render_template('index.html', books=books)

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)
