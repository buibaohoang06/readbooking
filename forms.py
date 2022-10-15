#Create WebForms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, InputRequired, Length
from flask_wtf.file import FileField
from models import User
from flask_ckeditor import CKEditorField

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired()], render_kw={"placeholder": "Password"})
    email = StringField(validators=[InputRequired()], render_kw={"placeholder": "Email"})
    submit = SubmitField()

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired()], render_kw={"placeholder": "Password"})
    email = StringField(validators=[InputRequired()], render_kw={"placeholder": "Email"})
    submit = SubmitField()

    def validate_user(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("This username already exists")
        
class PostForm(FlaskForm):
    title = StringField(validators=[InputRequired()], render_kw={"placeholder": "Title"})
    content = CKEditorField(validators=[InputRequired()], render_kw={"placeholder": "Content"})
    description = StringField(validators=[InputRequired()], render_kw={"placeholder": "Description"})
    main_image = FileField("Main Image")
    submit = SubmitField(render_kw={"value": "Post"})

class SearchForm(FlaskForm):
    search_content = StringField(validators=[InputRequired()], render_kw={"placeholder": "What do you want to see today?"})
    submit = SubmitField(render_kw={"value": "Search"})