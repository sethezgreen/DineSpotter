from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import review
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# The above is used when we do login registration, flask-bcrypt should already be in your env check the pipfile

# Remember 'fat models, skinny controllers' more logic should go in here rather than in your controller. Your controller should be able to just call a function from the model for what it needs, ideally.

class User:
    db = "dine_spotter_schema" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.reviews = []
        # What changes need to be made above for this project?
        #What needs to be added here for class association?



    # Create Users Models

    @classmethod
    def create_user(cls, user_data):
        if not cls.validate_user(user_data):
            return False
        user_data = user_data.copy()
        user_data['password'] = bcrypt.generate_password_hash(user_data['password'])
        query = """
                INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
                ;"""
        user_id = connectToMySQL(cls.db).query_db(query, user_data)
        session['id'] = user_id # starts with the user logged in after registering
        session['first_name'] = user_data['first_name']
        return user_id

    # Read Users Models

    @classmethod
    def get_user_by_email(cls, email):
        data = {'email' : email}
        query = """
                SELECT *
                FROM users
                WHERE email = %(email)s
                ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            this_user = cls(result[0])
            return this_user
        return False
    
    @classmethod
    def get_id(cls, id):
        data = {'id' : id}
        query = """ SELECT * FROM users
                    WHERE id = %(id)s
                """
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            this_user = cls(result[0])
            return this_user
        return False
    
    @classmethod
    def get_user_with_reviews(cls, id):
        data = {'id': id}
        query = """
                SELECT *
                FROM users
                LEFT JOIN reviews
                ON reviews.user_id = %(id)s
                WHERE users.id = %(id)s
                ORDER BY reviews.created_at DESC
                ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        this_user = cls(results[0])
        for result in results:
            if result['reviews.id'] != None:
                one_review = review.Review({
                    'id': result['reviews.id'],
                    'user_id': result['user_id'],
                    'restaurant': result['restaurant'],
                    'location': result['location'],
                    'item_ordered': result['item_ordered'],
                    'item_review': result['item_review'],
                    'service_review': result['service_review'],
                    'description': result['description'],
                    'created_at': result['reviews.created_at'],
                    'updated_at': result['reviews.updated_at']
                })
                this_user.reviews.append(one_review)
        return this_user
    
    # Update Users Models



    # Delete Users Models



    # Login Methods
    @classmethod
    def login(cls, data):
        this_user = cls.get_user_by_email(data['email'])
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data['password']):
                session['id'] = this_user.id
                session['first_name'] = this_user.first_name
                return True
        flash("Invalid Login Information")
        return False



    # Validation
    @staticmethod
    def validate_user(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['email']) < 1:
            flash("Email required")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email")
            is_valid = False
        if User.get_user_by_email(data['email']):
            flash("Email taken")
            is_valid = False
        if len(data['first_name']) < 2:
            flash("First Name must be at least 2 characters")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last Name be at least 2 characters")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Passwords must match")
            is_valid = False
        return is_valid