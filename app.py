"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import DEFAULT_IMAGE_URL, db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.get('/')
def home_page():
    """Redirects to users page"""

    return redirect('/users')

@app.get('/users')
def list_users():
    """List users"""

    users = User.query.all()
    return render_template("list.html", users=users)

@app.get('/users/new')
def create_user_form():
    """Displays form to add a new user"""

    return render_template('form.html')

@app.post('/users/new')
def submit_user():
    """Form to create a new user"""


    first_name = request.form['first-name']
    last_name = request.form['last-name']
    img_url = request.form['img-url']
    img_url = img_url if img_url else None

    new_user = User(first_name=first_name,
                    last_name=last_name,
                    img_url=img_url)

    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@app.get('/users/<int:user_id>')
def show_user_details(user_id):
    """Shows user details"""

    user = User.query.get_or_404(user_id)
    return render_template('detail.html', user=user)


@app.get('/users/<int:user_id>/edit')
def show_edit_page(user_id):
    """Displays edit page"""

    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.post('/users/<int:user_id>/edit')
def submit_edit_page(user_id):
    """Submit edit details"""

    user = User.query.get_or_404(user_id)

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    img_url = request.form['img-url']
    img_url = img_url if img_url else DEFAULT_IMAGE_URL

    user.first_name = first_name
    user.last_name = last_name
    user.img_url = img_url


    # db.session.add(user)
    db.session.commit()
    return redirect('/users')


@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Handle form to delete user"""

    User.query.filter(User.id == user_id).delete()
    db.session.commit()

    return redirect('/users')
