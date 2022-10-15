#Admin Blueprint
#URL Prefix /admin

import sqlite3
from threading import currentThread
from flask import Blueprint, request, render_template, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required, login_manager
from models import db, User, Post
from forms import LoginForm, RegisterForm, PostForm
from flask_bcrypt import Bcrypt
from flask_ckeditor import CKEditor
from sqlalchemy import exc
from app import app
import uuid
from datetime import datetime
from flask_uploads import configure_uploads, IMAGES, UploadSet

#Initializing Admin Blueprint
adminbp = Blueprint('admin', __name__, static_folder="static", template_folder="templates", url_prefix="/admin")
#Initializing Dependencies
bcrypt = Bcrypt(app) #Password Encryptor
ckeditor = CKEditor(app) #CKEditor
images = UploadSet('images', IMAGES) #For image upload
configure_uploads(app, images) 

#Dashboard - Contains management tools
@adminbp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    user_current_session = User.query.filter_by(id=current_user.id).first()
    if user_current_session.is_admin:
        post_form = PostForm()
        if post_form.validate_on_submit():
            try:
                link = post_form.title.data.lower().replace(" ", "-")
                file_name = images.save(post_form.main_image.data)
                print(file_name)
                new_post = Post(author=user_current_session.username, link=link, description=post_form.description.data, title=post_form.title.data, content=post_form.content.data, time=datetime.now().replace(microsecond=0), image=file_name, uuid=str(uuid.uuid4()))
                db.session.add(new_post)
                db.session.commit()
                flash("Post Created!", 'success')
                return redirect('/admin/dashboard')
            except exc.IntegrityError as err: 
                db.session.rollback()
                flash("Looks like another post was created with the same title. Use a different title and try again!", 'warning')
                return redirect('/admin/dashboard')
            except Exception as e:
                db.session.rollback()
                print(str(e))
                flash("Error Occured: " + str(e), 'danger')
                return redirect('/admin/dashboard')
    else:
        flash('You don\'t have enough privilege to enter this page.', 'info')
        return redirect('/')
    return render_template('post.html', username=user_current_session.username, userid=user_current_session.userid, form=post_form, uuid=str(uuid.uuid4()))

