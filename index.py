#Index Blueprint
#URL Prefix: /
import sqlite3
from flask import Blueprint, request, render_template, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required, login_manager
from models import db, User, Post
from forms import LoginForm, RegisterForm, SearchForm
from flask_bcrypt import Bcrypt
from flask_ckeditor import CKEditor
from sqlalchemy import exc, desc
from app import app
import uuid
import datetime

indexbp = Blueprint("index", __name__, static_folder="static", template_folder="templates")

bcrypt = Bcrypt(app)
#Main page
@indexbp.route('/', methods=['GET', 'POST'])
def mainpage():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(desc(Post.id)).paginate(per_page=6, page=page)
    sform = SearchForm()
    username = ""
    queried_posts = ""
    if sform.validate_on_submit():
        queried_posts = Post.query.filter(Post.title.like("%" + sform.search_content.data + "%")).paginate(per_page=6, page=page)
        if current_user.is_authenticated:
            user_current_session = User.query.filter_by(id=current_user.id).first()
            username = user_current_session.username
    else:
        if current_user.is_authenticated:    
            user_current_session = User.query.filter_by(id=current_user.id).first()
            username = user_current_session.username
    return render_template('mainpage.html', posts=posts, username=username, sform=sform, queried_posts=queried_posts)

#Display posts
@indexbp.route('/posts/<post_url>', methods=['GET', 'POST'])
def index(post_url):
    try:
        if current_user.is_authenticated:
            user_current_session = User.query.filter_by(id=current_user.id).first()
            username = user_current_session.username
        post = Post.query.filter_by(link=post_url).first()
        if post == None:
            flash('We can\'t find the specified post. Please try again with a different link!', 'warning')
            db.session.rollback()
            return redirect('/')
    except Exception as e:
        db.session.rollback()
        flash('Something went wrong! Contact admins if this problem persists!', 'danger')
        return redirect('/')
    return render_template("displayposts.html", post=post, username=username)

@indexbp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    login_form = LoginForm()
    if login_form.validate_on_submit():
        try:
            query_user = User.query.filter_by(username=login_form.username.data, email=login_form.email.data).first()
            if bcrypt.check_password_hash(query_user.hashed_password, login_form.password.data):
                login_user(query_user)
                flash("Login Successful", 'success')
                return redirect('/')
        except AttributeError:
            db.session.rollback()
            flash("Incorrect Username, Password or Email", 'danger')
            return redirect('/login')
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return redirect('/login')

    return render_template("login.html", form=login_form)

@indexbp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        try:
            new_user = User(username=register_form.username.data, hashed_password=bcrypt.generate_password_hash(register_form.password.data), email=register_form.email.data, userid=str(uuid.uuid4()), is_admin=True)
            db.session.add(new_user)
            db.session.commit()
            flash("Account creation successful! Login to continue.", 'success')
            return redirect('/login')
        except Exception as e:
            print(str(e))
            flash("Error occured - Check if your username already exists, or something is wrong with the server.", 'danger')
            db.session.rollback()
            return redirect('/register')

    return render_template('register.html', form=register_form)


@indexbp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/login')


