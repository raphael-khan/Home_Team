from app import app
from flask import Flask, render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
from app.models.user import User

bcrypt = Bcrypt(app)

#-------- main landing page. Containers login & registration.
@app.route('/')
def index():
    return render_template('index.html')

#-------- hidden route that validdates form data, registers and logs in. 
@app.route("/register", methods=['POST'])
def register():
    is_valid = User.validate(request.form)
    if not is_valid:
        return redirect('/')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    if not id:
        flash('something went wrong')
        return redirect('/')
    session['user_id'] = id
    return redirect('/dashboard')

# Login Route -- change based on username or email 
@app.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    user = User.get_email(data)
    if not user:
        flash("Invalid Login Credentials")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Wrong password")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

#Logout Route. 
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')