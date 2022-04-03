from app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from app.models import user

# class modelled after the database table.
class Listing:
    db_name = 'sell_fast'
    def __init__(self, data):
        self.id = data['id']
        self.property_name = data['property_name']
        self.property_type = data['property_type']
        self.address = data['address']
        self.year_built = data['year_built']
        self.price = data['price']
        self.description = data['description']
        self.image = data['image']
        self.number_of_bedrooms = data['number_of_bedrooms']
        self.number_of_bathrooms = data['number_of_bathrooms']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

# static mehtod to validate the Listings. 
    @staticmethod
    def validate(listing):
        is_valid = True
        if 'property_type' not in listing:
            is_valid = False
            flash('Please enter a property type')
        if listing['address'] == '':
            is_valid = False
            flash('Please enter an address for the property')
        if listing['year_built'] =='':
            is_valid = False
            flash('Please enter the year property of built in')
        if listing['price'] == '':
            is_valid = False
            flash('Please enter a valid price')
        if listing['description'] == '':
            is_valid = False
            flash('Please enter a description for the property')
        return is_valid

# class method to save a Listing. 
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO listings (property_name, property_type, year_built, price, description, number_of_bedrooms, number_of_bathrooms, address, image, users_id) VALUES ( %(property_name)s, %(property_type)s, %(year_built)s, %(price)s, %(description)s, %(number_of_bedrooms)s, %(number_of_bathrooms)s, %(address)s, %(image)s, %(users_id)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)

# class method to delete a listing.
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM listings WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

# class method to retrive one listing.
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM listings WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

# class method to update a user. 
    @classmethod
    def update(cls, data):
        q = "UPDATE listings SET property_name=%(property_name)s, price=%(price)s, description=%(description)s, address=%(address)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(q, data)


    @classmethod
    def get_oneW_user(cls,data):
        q = "SELECT * FROM listings LEFT JOIN users on listings.users_id = users.id WHERE listings.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(q,data)
        one_listing = cls(results[0])
        one_listing.user = user.User.get_one({'id': results[0]['users_id']})
        return one_listing
        