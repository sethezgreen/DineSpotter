from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

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
        if not cls.validate_diner(data):
            return False
        query = """ INSERT INTO reviews(user_id, restaurant, location, item_ordered, item_review, service_review, description) 
                    VALUES(%(user_id)s, %(restaurant)s, %(location)s, %(item_ordered)s, %(item_review)s, %(service_review)s, %(description)s)
                """
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_id(cls,id):
        query = """ SELECT * FROM reviews
                    JOIN users on reviews.user_id = users.id
                    WHERE reviews.id = %(id)s
                """
        data = {'id':id}
        results = connectToMySQL(cls.db).query_db(query, data)[0]
        review = Review(results)
        review.user = User({
            'id':results['id'],
            'first_name':results['first_name'],
            'last_name':results['last_name'],
            'email':results['email'],
            'password':results['password']
        })
        return review
    
    @classmethod
    def get_all(cls):
        query = """ SELECT * FROM reviews
                    JOIn users on reviews.user_id = users.id
                """
        results = connectToMySQL(cls.db).query_db(query)
        reviews = []
        for result in results:
            review = Review(result)
            review.user = User({
                'id':result['id'],
            'first_name':result['first_name'],
            'last_name':result['last_name'],
            'email':result['email'],
            'password':result['password']
            })
            reviews.append(review)
        return reviews
    
    @classmethod
    def edit_review(cls,id):
        query = """ UPDATE reviews
                    SET restaurant = %(restaurant)s,location = %(location)s,item_ordered = %(item_ordered)s,item_review = %(item_review)s,service_review = %(service_review)s,description = %(description)s
                    WHERE id = %(id)s 
                """
        result = connectToMySQL(cls.db).query_db(query, id)
        return result
    
    @classmethod
    def delete_review(cls, id):
        query = """ DELETE FROM reviews
                    WHERE id = %(id)s
                """
        data = {'id':id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result

    @staticmethod
    def validate_diner(diner):
        is_valid = True
        if 1 > len(diner['restaurant']) > 45:
            flash('Restaurant name must be between 1-45 characters')
            is_valid = False
        if 1 > len(diner['location']) > 45:
            flash('Location must be between 1-45 characters')
            is_valid = False
        if 1 > len(diner['item_ordered']) > 45:
            flash('Item name must be between 1-45 characters')
            is_valid = False
        if 1 > diner['item_review'] > 5:
            flash('Please rate item from 1-5')
            is_valid = False
        if 1 > diner['service_review'] > 5:
            flash('Please rate service from 1-5')
            is_valid = False
        if len(diner['description']) < 1:
            flash('Please add a description')
            is_valid = False
        return is_valid