from . import bp as auth
from app import db, mail
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required
from flask_mail import Message
from .forms import UserInfoForm, LoginForm
from .models import User


@auth.route('/register', methods=["GET", 'POST'])
def register():
    register_form = UserInfoForm()
    if register_form.validate_on_submit():
        # Grab Data from form
        username = register_form.username.data
        email = register_form.email.data
        password = register_form.password.data

        # Check if the username from the form already exists in the User table
        existing_user = User.query.filter_by(username=username).all()
        # If there is a user with that username message them asking them to try again
        if existing_user:
            # Flash a warning message
            flash(f'The username {username} is already registered. Please try again.', 'danger')
            # Redirect back to the register page
            return redirect(url_for('auth.register'))

        # Create a new user instance
        new_user = User(username, email, password)
        # Add that user to the database
        db.session.add(new_user)
        db.session.commit()
        # Flash a success message thanking them for signing up
        flash(f'Thank you {username}, you have succesfully registered!', 'success')

        # # Create Welcome Email to new user
        # welcome_message = Message('Welcome to the Kekambas Blog!', [email])
        # welcome_message.body = f'Dear {username}, Thank you for signing up for our blog. We are so excited to have you.'

        # # Send Welcome Email
        # mail.send(welcome_message)

        # Redirecting to the home page
        return redirect(url_for('index'))
        
    return render_template('register.html', form=register_form)



@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Grab data from form
        username = form.username.data
        password = form.password.data

        # Query our User table for a user with username
        user = User.query.filter_by(username=username).first()

        # Check if the user is None or if password is incorrect
        if user is None or not user.check_password(password):
            flash('Your username or password is incorrect', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user)

        flash(f'Welcome {user.username}. You have succesfully logged in.', 'success')

        return redirect(url_for('index'))
        

    return render_template('login.html', login_form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@auth.route('/my-account')
@login_required
def my_account():
    return render_template('my_account.html')
