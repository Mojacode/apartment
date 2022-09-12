from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash

class Room:
    def __init__(self, data):
        self.id = data['id']
        self.shortdetail = data['shortdetail']
        self.details = data['details']
        self.location = data['location']
        self.status = data['status']
        self.rent = data['rent']
        self.rentedby = data['rentedby']
        self.users_id = data['users_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def saveRoom(cls,data):
        query = "INSERT INTO apartment.rooms (shortdetail, details, location, status, rent, rentedby ,users_id, created_at, updated_at) VALUES (%(shortdetail)s, %(details)s, %(location)s, %(status)s, %(rent)s , %(rentedby)s, %(users_id)s, NOW(),NOW());"
        return connectToMySQL("apartment").query_db(query, data)
    
    @classmethod
    def get_all(cls, data):
        query = "SELECT * from apartment.rooms INNER JOIN apartment.users on users.id = rooms.users_id WHERE users.id = %(users_id)s; "
        results = connectToMySQL("apartment").query_db(query,data)
        all_rooms = []
        for room in results:
            print(room)
            all_rooms.append(cls(room))
        return all_rooms
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * from apartment.rooms INNER JOIN apartment.users on users.id = rooms.users_id WHERE rooms.id = %(id)s;"
        results = connectToMySQL("apartment").query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def update_room(cls,data):
        query = "UPDATE apartment.rooms SET shortdetail=%(shortdetail)s, details=%(details)s, location=%(location)s, status=%(status)s,rent=%(rent)s,rentedby=%(rentedby)s, updated_at= NOW() WHERE id = %(id)s;"
        return connectToMySQL("apartment").query_db(query, data)
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM apartment.rooms WHERE id = %(id)s;"
        return connectToMySQL('apartment').query_db(query,data)