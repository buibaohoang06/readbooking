from app import app
from index import indexbp
from admin import adminbp
from flask_login import LoginManager
from models import db, User

app.register_blueprint(indexbp)
app.register_blueprint(adminbp)

lm = LoginManager()
lm.init_app(app)
lm.login_view = "login"

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)