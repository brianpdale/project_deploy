from flask import flash
from flask_bcrypt import Bcrypt

import re
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from ..models import user

bcrypt = Bcrypt(app)

class Show:
    def __init__(self, data):

        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        if 'user' in data:
            self.user = data['user']

    @classmethod    
    def get_all_shows(cls):
        query = "SELECT * FROM tv_shows"
        tv_shows_from_db = connectToMySQL('tv_shows_schema').query_db(query)
        shows = []
        for show in tv_shows_from_db:
            shows.append(cls(show))
        return shows

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM tv_shows WHERE id = %(id)s;"
        results = connectToMySQL("tv_shows_schema").query_db(query, data)

        results_data = {
            "id": results[0]['id'],
            "title": results[0]['title'],
            "network": results[0]['network'],
            "release_date": results[0]['release_date'],
            "description": results[0]['description'],
            "created_at": results[0]['created_at'],
            "updated_at": results[0]['updated_at'],
            "user": user.User.get_by_id({"id": results[0]['user_id']})
            }
        return cls(results_data)


    @classmethod
    def update_show(cls, data):
        query = "UPDATE tv_shows SET title = %(title)s, network = %(network)s, release_date = %(release_date)s, "\
                "description = %(description)s, updated_at = NOW() WHERE id = %(id)s;"
        show = connectToMySQL("tv_show_schema").query_db(query, data)

        return show

    @classmethod
    def create(cls, data):
        query = "INSERT INTO tv_shows (user_id, title, network, release_date, description, created_at, updated_at) "\
            "VALUES (%(user_id)s, %(title)s, %(network)s, %(release_date)s, %(description)s, NOW(), NOW());"
        show_id = connectToMySQL("tv_shows_schema").query_db(query, data)

        return show_id

    @classmethod
    def update_show(cls, data):
        query = "UPDATE tv_shows SET title = %(title)s, network = %(network)s, release_date = "\
            " %(release_date)s, description = %(description)s, updated_at = NOW() WHERE id = %(id)s;"
        show_id = connectToMySQL("tv_shows_schema").query_db(query, data)

        return show_id

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM tv_shows WHERE id = %(id)s;"
        connectToMySQL("tv_shows_schema").query_db(query, data)


    @staticmethod
    def show_validator(post_data):
        is_valid = True

        if len(post_data['title']) < 3:
            flash("Tv Show name must be at least 3 characters.")
            is_valid = False
        
        if len(post_data['network']) < 3:
            flash("Tv Show network must be at least 3 characters.")
            is_valid = False

        if len(post_data['description']) < 3:
            flash("Tv Show description must be at least 3 characters.")
            is_valid = False

        if len(post_data['release_date']) < 10:
            flash("Tv Show release date must be at least 10 characters.")
            is_valid = False

        return is_valid
            

