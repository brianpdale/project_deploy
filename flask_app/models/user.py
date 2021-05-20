from flask import flash
from flask_bcrypt import Bcrypt

import re
from flask_app import app
from flask_app.models.show import Show
from flask_app.config.mysqlconnection import connectToMySQL

bcrypt = Bcrypt(app)

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password= data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.show = []

    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users LEFT JOIN tv_shows ON users.id = tv_shows.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL("tv_shows_schema").query_db(query, data)

        user = cls(results[0])
        if results[0]['tv_shows.id'] != None:
            for row in results:
                row_data = {
                    'id': row['tv_shows.id'],
                    'title': row['title'],
                    'network': row['network'],
                    'release_date': row['release_date'],
                    'description': row['description'],
                    'created_at': row['tv_shows.created_at'],
                    'updated_at': row['updated_at']
                    
                }
                user.show.append(Show(row_data))

        return user

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) "\
            "VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        user_id = connectToMySQL("tv_shows_schema").query_db(query, data)

        return user_id

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users where email = %(email)s;"
        results = connectToMySQL("tv_shows_schema").query_db(query, data)

        return cls(results[0]) if len(results) > 0 else None

    @staticmethod
    def register_validator(post_data):
        is_valid = True

        if len(post_data['first_name']) < 2:
            flash("First Name must be more than 2 characters.")
            is_valid = False
        
        if len(post_data['last_name']) < 2:
            flash("Last Name must be more than 2 characters.")
            is_valid = False

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            flash("Invalid email.")
            is_valid = False

        if len(post_data['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False

        if post_data['password'] != post_data['confirm_password']:
            flash("Password and Confirm password must match")
            is_valid = False

        return is_valid
            

    @staticmethod
    def login_validator(post_data):
        user = User.get_by_email({"email": post_data['email']})

        if not user:
            flash("Invalid credentials")
            return False
        
        if not bcrypt.check_password_hash(user.password, post_data['password']):
            flash("Invalid credentials")
            return False

        return True
