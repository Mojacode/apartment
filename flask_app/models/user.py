from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)  


class User:
    def __init__(self, data):
        self.id = data['id']
        self.fname = data['fname']
        self.lname = data['lname']
        self.email = data['email']
        self.password = data['password']
        self.usertype = data['usertype']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @staticmethod
    def validate_register(user):
        # connect to db to check for existing user
        query = "SELECT * FROM apartment.users WHERE email = %(email)s;"
        results = connectToMySQL("apartment").query_db(query,user)
        # Validation
        is_valid = True # we assume this is true
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","register")
            is_valid = False
        if len(user['fname']) < 3:
            flash("First Name must be at least 3 characters.")
            is_valid = False
        if len(user['lname']) < 3:
            flash("Last name must be at least 3 characters.")
            is_valid = False
        if len(user['email']) < 8:
            flash("Email must be at least 8 characters.")
            is_valid = False
        if len(user['password']) < 3:
            flash("Password must be at least 3 characters.")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Password does not match")
            is_valid = False
        if user['usertype'] == None:
            flash('Please Pick User type')
            is_valid = False
        return is_valid

    @classmethod
    def save(cls,data):
        query = "INSERT INTO apartment.users (fname, lname, email, password, usertype, created_at, updated_at) VALUES (%(fname)s,%(lname)s,%(email)s, %(password)s, %(usertype)s, NOW(),NOW());"
        return connectToMySQL("apartment").query_db(query, data)
    
    @classmethod
    def validate_email(cls,data):
        query = "SELECT * FROM apartment.users WHERE email = %(email)s;"
        results = connectToMySQL("apartment").query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])


    @classmethod
    def get_id(cls,data):
        query = "SELECT * FROM apartment.users WHERE id = %(users_id)s;"
        results = connectToMySQL("apartment").query_db(query,data)
        return cls(results[0])

    