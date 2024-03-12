from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user

class Review:
    db = "dine_spotter_schema"
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.restaurant = data['restaurant']
        self.location = data['location']
        self.item_ordered = data['item_ordered']
        self.item_review = data['item_review']
        self.service_review = data['service_review']
        self.description = data['description']
        self.user = None

    @classmethod
    def new_review(cls,data):
        if not cls.validate_review(data):
            return False
        data = data.copy()
        data['user_id'] = session['id']
        query = """ INSERT INTO reviews(user_id, restaurant, location, item_ordered, item_review, service_review, description) 
                    VALUES(%(user_id)s, %(restaurant)s, %(location)s, %(item_ordered)s, %(item_review)s, %(service_review)s, %(description)s)
                ;"""
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_review_by_id(cls,id):
        query = """ 
                SELECT * 
                FROM reviews
                JOIN users on reviews.user_id = users.id
                WHERE reviews.id = %(id)s
                ;"""
        data = {'id':id}
        results = connectToMySQL(cls.db).query_db(query, data)[0]
        review = Review(results)
        review.user = user.User({
            'id':results['users.id'],
            'first_name':results['first_name'],
            'last_name':results['last_name'],
            'email':results['email'],
            'password':results['password'],
            'created_at': results['users.created_at'],
            'updated_at': results['users.updated_at']
        })
        return review
    
    @classmethod
    def get_all(cls):
        query = """ SELECT * FROM reviews
                    JOIN users on reviews.user_id = users.id
                ;"""
        results = connectToMySQL(cls.db).query_db(query)
        reviews = []
        for result in results:
            review = Review(result)
            review.user = user.User({
                'id':result['users.id'],
                'first_name':result['first_name'],
                'last_name':result['last_name'],
                'email':result['email'],
                'password':result['password'],
                'created_at':result['users.created_at'],
                'updated_at':result['users.updated_at']
            })
            reviews.append(review)
        return reviews
    
    @classmethod
    def edit_review(cls,id):
        if not cls.validate_review(id):
            return False
        query = """ UPDATE reviews
                    SET restaurant = %(restaurant)s,location = %(location)s,item_ordered = %(item_ordered)s,item_review = %(item_review)s,service_review = %(service_review)s,description = %(description)s
                    WHERE id = %(id)s 
                ;"""
        result = connectToMySQL(cls.db).query_db(query, id)
        return result
    
    @classmethod
    def delete_review(cls, id):
        query = """ DELETE FROM reviews
                    WHERE id = %(id)s
                ;"""
        data = {'id':id}
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @staticmethod
    def validate_review(data):
        is_valid = True
        if 1 > len(data['restaurant']) > 45:
            flash('Restaurant name must be between 1-45 characters')
            is_valid = False
        if 1 > len(data['location']) > 45:
            flash('Location must be between 1-45 characters')
            is_valid = False
        if 1 > len(data['item_ordered']) > 45:
            flash('Item name must be between 1-45 characters')
            is_valid = False
        if isinstance(data['item_review'], int):
            if 1 > data['item_review'] > 5:
                flash('Please rate item from 1-5')
                is_valid = False
        elif len(data['item_review']) < 1:
                flash('Please rate item from 1-5')
                is_valid = False
        if isinstance(data['service_review'], int):
            if 1 > data['service_review'] > 5:
                flash('Please rate item from 1-5')
                is_valid = False
        elif  len(data['service_review']) < 1:
            flash('Please rate service from 1-5')
            is_valid = False
        if len(data['description']) < 1:
            flash('Please add a description')
            is_valid = False
        return is_valid