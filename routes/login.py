from flask import Blueprint, render_template, redirect, url_for

login = Blueprint('login', __name__)

@login.route('/login')
def login_page():
    return render_template('login.html')

@login.route('/register')
def register():
    return render_template('register.html')

@login.route('/logout')
def logout():
    return redirect(url_for('main.index'))
