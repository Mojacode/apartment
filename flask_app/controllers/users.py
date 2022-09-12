from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.room import Room
from flask_bcrypt import Bcrypt  
bcrypt = Bcrypt(app)  



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registration')
def registration_form():
    return render_template('registration.html')

@app.route('/registered', methods = ['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/registration')
    pw_hash= bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data = {
        "fname": request.form['fname'],
        "lname": request.form['lname'],
        "email": request.form['email'],
        "password": pw_hash,
        "usertype": request.form['usertype']
        }
    user_id = User.save(data)
    session['id'] = user_id
    return redirect('/')

@app.route('/login', methods = ['POST'])
def login():
    user = User.validate_email(request.form)
    if not user:
        flash("Email Not Found")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password")
        return redirect('/')
    session['user_id'] = user.id
    if user.usertype == "tenant":
        return redirect ('/myRoom')
    else:
        return redirect('/roomList')
    

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/market')
def market():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'users_id' : session['user_id']
    }
    return render_template('market.html', user= User.get_id(data))




# LANDLORD LOGIN
@app.route('/roomList')
def LandlordDashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'users_id' : session['user_id']
    }
    type = User.get_id(data)
    if type.usertype != "landlord":
        return redirect('/')
    return render_template('roomList.html', user= User.get_id(data), room = Room.get_all(data))

@app.route('/addRoom')
def addRoomForm():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'users_id' : session['user_id']
    }
    type = User.get_id(data)
    if type.usertype != "landlord":
        return redirect('/')
    return render_template('addRoom.html')

# Tenant ROUTES
@app.route('/myRoom')
def myRoom():
    # use session to show users room
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'users_id' : session['user_id']
    }
    return render_template('myRoom.html', user = User.get_id(data))
