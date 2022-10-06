from flask_app.config.mysqlconnection import connectToMySQL


from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class Chef:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes_posted = []


    @classmethod
    def register_chef(cls, data):
        query = "INSERT INTO chefs (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        results = connectToMySQL('recipes_core').query_db(query, data)
        print(results)
        return results 

    @classmethod
    def get_all_chefs(cls):
        query = "SELECT * FROM chefs;" 
        results = connectToMySQL('recipes_core').query_db(query)
        print(results)
        all_chefs = []
        for one_chef in results:
            all_chefs.append(cls(one_chef))
        return all_chefs


    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM chefs WHERE email = %(email)s;"
        results = connectToMySQL('recipes_core').query_db(query, data)
        print(results)
        if results == ():
            return False
        return cls(results[0])


    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM chefs WHERE id = %(id)s;"
        results = connectToMySQL('recipes_core').query_db(query, data)
        print(results)
        return cls(results[0])


    @staticmethod
    def validate_create(user):
        is_valid = True
        if len(user['email']) < 6:
            flash("*Email is too short")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("*Email is not correct format")
            is_valid = False
        if not re.match(r'^[a-zA-Z\s]+$', user['first_name']):
            flash("*First name must contain only letters")
            is_valid = False
        if not re.match(r'^[a-zA-Z\s]+$', user['last_name']):
            flash("*Last name must contain only letters")
            is_valid = False    
        if len(user['password']) < 8:
            flash("*Password must be 8 characters or more")
            is_valid = False    
        if user['password'] != user['conf_password']:
            flash("*Confirm Password does not match password")
            is_valid = False
        data = {
            "email": user['email']
        }    
        chef_in_db = Chef.get_by_email(data)
        print(chef_in_db)    
        if chef_in_db:
            flash("*Email already taken")
            is_valid = False
        return is_valid        


