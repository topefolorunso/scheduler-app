from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import Users
from .. import db

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['POST', 'GET'])
def signup():

    if request.method == 'POST':
        user_email = request.form['email']
        user_nick = request.form['nick']
        user_password = request.form['password']

        hashed_password = generate_password_hash(user_password, method='sha256')

        user = Users.query.filter_by(email=user_email).first()
        if user:
            flash('Email address already exists')
            return redirect('/signup')

        new_user = Users(email=user_email, nick=user_nick, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')

    return render_template('signup.html')

@auth.route('/login', methods=['POST', 'GET'])
def login():
    
    if request.method =='POST':
        user_email = request.form['email']
        user_password = request.form['password']
        try:
            remember = True if request.form['remember'] else False
        except:
            remember = False

        print(remember)

        user = Users.query.filter_by(email=user_email).first()
        if not user:
            flash('Invalid credentials')
            return redirect('/login')
        if not check_password_hash(user.password, user_password):
            flash('Invalid credentials')
            return redirect('/login')

        login_user(user, remember=remember)
        return redirect('/home')

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')