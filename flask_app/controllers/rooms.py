import re
from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.room import Room
from flask_app.models.user import User

@app.route('/saveRoom', methods = ['POST'])
def saveRoom():
    if 'user_id' not in session:
        return redirect ('/')

    data={
        "shortdetail": request.form['shortdetail'],
        "details": request.form['details'],
        "location": request.form['location'],
        "status" : request.form['status'],
        "rent": request.form['rent'],
        "rentedby": request.form['rentedby'],
        "users_id": session['user_id']
    }
    Room.saveRoom(data)
    return redirect('/roomList')

@app.route('/showRoom/<int:room_id>')
def showRoom(room_id):
    if 'user_id' not in session:
        return redirect ('/')

    data ={
        "id" : room_id,
        "users_id": session['user_id']
    }
    return render_template('showRoom.html', user= User.get_id(data), room = Room.get_one(data))

@app.route('/editRoom/<int:room_id>')
def editRoom(room_id):
    if 'user_id' not in session:
        return redirect ('/')
    data ={
        "id" : room_id,
        "users_id": session['user_id']
    }
    type = User.get_id(data)
    if type.usertype != "landlord":
        return redirect('/')

    return render_template('editRoom.html', user= User.get_id(data), room = Room.get_one(data))

@app.route("/editedRoom", methods=["POST"])
def editedRoom():
    if 'user_id' not in session:
        return redirect ('/')

    data={
        "shortdetail": request.form['shortdetail'],
        "details": request.form['details'],
        "location": request.form['location'],
        "status" : request.form['status'],
        "rent": request.form['rent'],
        "rentedby": request.form['rentedby'],
        "id": request.form['id']
    }
    Room.update_room(data)
    return redirect("/roomList")

@app.route('/delete/<int:id>')
def delete(id):

    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": id
    }
    Room.delete(data)
    return redirect('/roomList')