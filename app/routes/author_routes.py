from flask import Blueprint, render_template, request, redirect, url_for
from app.models.authors import Author
from app import db
from app.models.users import User

bp = Blueprint('author', __name__, url_prefix='/Author')

@bp.route('/')
def index():
    authors = Author.query.all()   
    return render_template('authors/index.html', data=authors)

@bp.route('/list/<int:id>', methods=['GET'])
def list(id):
    author = Author.query.get_or_404(id)
    books = author.books
    return render_template('authors/list.html ',books=books)

@bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nameUser = request.form['username']
        passwordUser = request.form['password']
        email = request.form['email']
        new_user = User(nameUser=nameUser, passwordUser=passwordUser, email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('user.index'))

    return render_template('Users/add.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    User = User.query.get_or_404(id)

    if request.method == 'POST':
        User.username = request.form['username']
        User.email = request.form['email']
        User.password = request.form['password']
        db.session.commit()
        return redirect(url_for('user.index'))

    return render_template('Users/edit.html', user=User)
    

@bp.route('/delete/<int:id>')
def delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('user.index'))