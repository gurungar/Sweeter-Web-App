from flask import render_template, redirect, flash, url_for
from sweeter.forms import RegisterForm, LoginForm
from sweeter import app, db, bcrypt
from sweeter.models import User, Post



posts = [
    {
        'author': "Arjun Gurung",
        'title': 'Blog Post 1',
        'content': 'First Post Content',
        'date posted': 'February 15, 2019'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second Post Content',
        'date posted': 'February 16, 2019'
    }

]



@app.route("/")
@app.route("/index/")
def index():
    # return "Welcome to Sweeter - simpler version of twitter!"
    return render_template("index.html", posts=posts)


@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(f'You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash(f'Log in Unsuccessful!', 'danger')
    return render_template("login.html", title='Login', form=form)


@app.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Your Account has been created! You can now log in!', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title='Register', form=form)
