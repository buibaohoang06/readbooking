from flask import Flask
#Initializing App
app = Flask(__name__)
#Entering configurations
#Change SECRET_KEY on production deployment
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SECRET_KEY'] = "testkey"
app.config['UPLOADED_IMAGES_DEST'] = 'static/uploads/images'

