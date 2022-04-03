from app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from app.models import listing
from app.models.listing import Listing

# class modelled after the database table. 
class User:
    db_name ='sell_fast'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.listings = []

# static methdod to validate form data
    @staticmethod
    def validate(user):
        is_valid = True
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL('sell_fast').query_db(query, user)
        if len(results) >= 1:
            is_valid = False
            flash('Email address already exits. Please use another email')
        if len(user['first_name']) < 3:
            is_valid = False
            flash('First Name must be 4 characters long')
        if len(user['last_name']) < 3:
            is_valid = False
            flash('Last Name must 4 characters long')
        if not EMAIL_REGEX.match(user['email']):
            is_valid = False
            flash("Please enter a valid email address")
        if len(user['password']) < 8:
            is_valid = False
            flash('Password must be at least 8 characters long')
        if user['password'] != user['confirm']:
            is_valid = False
            flash("Passwords must match.")
        return is_valid

# class method to save data into the database. 
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)

# class method to retrive all users.
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

# class method to retrive one user.
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

# class method to delete a user.
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

# class method to get a user by email.
    @classmethod
    def get_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
# class method associating the two tables.
    @classmethod
    def get_all_users_listing(cls):
        query = "SELECT * FROM users JOIN listings ON users.id = listings.users_id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        print(results)
        all_listings = []
        for row in results:
            user_instance = User(row)
            data = {
                'id':row['listings.id'],
                'property_name':row['property_name'],
                'property_type':row['property_type'],
                'address':row['address'],
                'year_built':row['year_built'],
                'price':row['price'],
                'description':row['description'],
                'image':row['image'],
                'number_of_bedrooms':row['number_of_bedrooms'],
                'number_of_bathrooms':row['number_of_bathrooms'],
                'created_at':row['listings.created_at'],
                'updated_at': row['listings.updated_at']
            }
            user_instance.listing = Listing(data)
            all_listings.append(user_instance)
        return all_listings