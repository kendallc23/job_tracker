from flask import Blueprint, render_template, redirect, url_for, flash, request, render_template_string
from extensions import db, bcrypt, login_manager
from models import User, Part, Job
from forms import RegisterForm, LoginForm, PasswordResetRequestForm, PasswordResetForm, JobDataForm, NewPartForm
from flask_login import login_user, login_required, logout_user, current_user
from flask_mailman import EmailMessage
from reset_pass_html_content import email_html_content


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

    return render_template('auth/login.html', form=form)


@main.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@main.route('/job_data', methods=['GET', 'POST'])
@login_required
def job_data():
    parts = Part.query.all()
    part_choices = [(str(p.id), p.part_name) for p in parts]
    form = JobDataForm()
    form.part_id.choices = part_choices
    if request.method == 'POST':
        # get data from hidden form
        part_id = request.form.get('part_id')
        num_batches = int(request.form.get('num_batches'))
        num_per_batch = int(request.form.get('num_per_batch'))
        task = request.form.get('task')
        paint_type = request.form.get('paint_type')
        total_time = float(request.form.get('total_time'))
        avg_time_per_batch = float(request.form.get('avg_time_per_batch'))
        avg_time_per_part = float(request.form.get('avg_time_per_part'))

        # get part name
        part = Part.query.get(part_id)
        part_name = part.part_name if part else None

        # save data to Job table
        new_job = Job(
            user_id=current_user.id,
            part_id=part_id,
            part_name=part_name,
            num_batches=num_batches,
            num_per_batch=num_per_batch,
            task=task,
            paint_type=paint_type,
            total_time=total_time,
            avg_time_per_batch=avg_time_per_batch,
            avg_time_per_part=avg_time_per_part
        )
        db.session.add(new_job)
        db.session.commit()
        flash("Job data saved!")
        if current_user.role == "admin":
            return redirect(url_for('main.admin_dash'))
        return redirect(url_for('main.user_dash'))
    return render_template('data/job_data.html', form=form)


###### Request and Reset Password ######
def send_reset_password_email(user):
    # create reset password url with unique token
    reset_pass_url = url_for('main.reset_password',
                             token=user.generate_password_token(),
                             user_id=user.id,
                             _external=True)
    # create email message containing special url
    email_body = render_template_string(email_html_content,
                                        reset_pass_url=reset_pass_url)
    msg = EmailMessage(subject="Password Reset",
                       body=email_body,
                       to=[user.email])
    msg.content_subtype = "html"
    # sends message to email address input by user
    msg.send()


@main.route("/request_new_pass", methods=['GET', 'POST'])
def request_new_pass():
    form = PasswordResetRequestForm()
    # check if email corresponds to an existing user...

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        # if so, send password reset link
        if user:
            send_reset_password_email(user)

        # direct user to check email for link
        flash("Instructions to reset your password were sent to your email address, if it exists in our system.")

        return redirect(url_for("main.request_new_pass"))

    return render_template('auth/request_new_pass.html', form=form)


@main.route('/reset_password/<token>/<int:user_id>', methods=['GET', 'POST'])
def reset_password(token, user_id):
    # validate password reset token
    user = User.validate_reset_pass_token(token, user_id)
    #   error if unable to validate
    if user is None:
        return render_template('reset_pass_error.html')
    # take new password from form; hash password; update database
    form = PasswordResetForm()

    if form.validate_on_submit():
        # create hash encoding for new password and update user database with this value
        hashed_new_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_new_password
        db.session.commit()
        return render_template('reset_pass_success.html')

    # reset password page (pre submission)
    return render_template('auth/reset_password.html', form=form)


##### Application Routing (User Features) #####


@main.route('/user_dash', methods=['GET', 'POST'])
@login_required
def user_dash():
    return render_template('dash/user_dash.html')


##### Application Routing (Admin Features) #####
@main.route('/admin_dash', methods=['GET', 'POST'])
@login_required
def admin_dash():
    if current_user.role != "admin":
        flash("Access denied.")
        return redirect(url_for('main.user_dash'))
    return render_template('dash/admin_dash.html')


@main.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if current_user.role != "admin":
        flash("Access denied.")
        return redirect(url_for('main.user_dash'))
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
        # redirect to list of users
        return redirect(url_for("main.overview_data"))

    return render_template('auth/register.html', form=form)


@main.route('/new_part', methods=['GET', 'POST'])
@login_required
def new_part():
    if current_user.role != "admin":
        flash("Access denied.")
        return redirect(url_for('main.user_dash'))

    form = NewPartForm()

    # create new part to add to Part table
    if form.validate_on_submit():
        new_part = Part(part_name=form.part_name.data,
                        surface_area=form.surface_area.data)
        db.session.add(new_part)
        db.session.commit()
        # redirect to admin dashboard
        return redirect(url_for("main.admin_dash"))

    return render_template('data/new_part.html', form=form)


@main.route('/overview_data', methods=['GET', 'POST'])
@login_required
def overview_data():
    if current_user.role != "admin":
        flash("Access denied.")
        return redirect(url_for('main.user_dash'))

    users = User.query.all()
    parts = Part.query.all()
    jobs = Job.query.all()
    return render_template('data/overview_data.html', users=users, parts=parts, jobs=jobs)


@main.route('/edit_user/<int:user_id>', methods=['POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    action = request.form['action']
    if action == "toggle_role":
        user.role = "admin" if user.role == "user" else "user"
    if action == "update_email":
        user.email = request.form["email"]
    db.session.commit()
    return redirect(url_for("main.overview_data"))


@main.route('/estimate', methods=['GET', 'POST'])
@login_required
def estimate():
    if current_user.role != "admin":
        flash("Access denied.")
        return redirect(url_for('main.user_dash'))
    return render_template('data/estimate.html')
