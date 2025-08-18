# Imports
from flask import Flask, render_template, url_for, redirect, flash
# from flask_login import login_user, login_required, logout_user, current_user
from models import User
from extensions import db, bcrypt, login_manager
from routes import main
from config import Config
from dotenv import load_dotenv
from flask_mailman import Mail


# create flask app (all app configurations take place here with app setup)
app = Flask(__name__)
app.config.from_object(Config)

mailman = Mail(app)

# initialize db, password encryption and login manager
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"

# register app blueprint (allows for app to be easily refrenced in routing file)
app.register_blueprint(main)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Run Application
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
