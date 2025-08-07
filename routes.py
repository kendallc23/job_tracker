from flask import Blueprint, render_template, redirect, url_for, flash, request
from extensions import db, bcrypt, login_manager
from models import User
from forms import RegisterForm, LoginForm
from flask_login import login_user, login_required, logout_user, current_user


main = Blueprint("main", __name__)

##### Application Routing (General) #####

# @app.route('/')
# def home():
#     return render_template('home.html')


# Home Screen is Log In (for now - if there is any public info, create a public dash w a login option)
@main.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)

                # admin user
                if user.role == "admin":
                    return redirect(url_for("main.admin_dash"))

                # regular user
                if user.role == "user":
                    return redirect(url_for("main.user_dash"))

    return render_template('login.html', form=form)


@main.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@main.route('/job_data', methods=['GET', 'POST'])
@login_required
def job_data():
    return render_template('job_data.html')

##### Application Routing (User Features) #####


@main.route('/user_dash', methods=['GET', 'POST'])
@login_required
def user_dash():
    return render_template('user_dash.html')


##### Application Routing (Admin Features) #####
@main.route('/admin_dash', methods=['GET', 'POST'])
@login_required
def admin_dash():
    return render_template('admin_dash.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    # create new user in database
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(first=form.first.data,
                        last=form.last.data,
                        email=form.email.data,
                        username=form.username.data,
                        password=hashed_password,
                        role=form.role.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("main.login"))

    # redirect to login page

    return render_template('register.html', form=form)


@main.route('/overview_data', methods=['GET', 'POST'])
@login_required
def overview_data():
    users = User.query.all()
    return render_template('overview_data.html', users=users)


@main.route('/estimate', methods=['GET', 'POST'])
@login_required
def estimate():
    return render_template('estimate.html')
