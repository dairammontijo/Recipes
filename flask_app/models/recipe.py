from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import chef

from flask import flash
import re


class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.cooking_time = data['cooking_time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.maker = None




    @classmethod
    def create(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date_made, cooking_time, chef_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(cooking_time)s, %(chef_id)s);"
        results = connectToMySQL('recipes_core').query_db(query, data)
        print(results)
        return results


    @classmethod
    def update(cls, data):
        query = "UPDATE recipes set name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, cooking_time = %(cooking_time)s WHERE id = %(id)s;"
        results = connectToMySQL('recipes_core').query_db(query, data)
        print(results)
        return results  


    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL('recipes_core').query_db(query, data)
        print(results)
        return results
    


    @classmethod
    def get_recipe(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL('recipes_core').query_db(query, data)
        print(results)
        return cls(results[0])


    @classmethod 
    def get_all_with_chefs(cls):
        query = "SELECT * FROM recipes JOIN chefs ON chefs.id = recipes.chef_id;" 
        results = connectToMySQL('recipes_core').query_db(query)
        print(results)
        all_recipes = []
        for row in results:
            one_recipe = cls(row)
            chef_data = {
                "id": row['chefs.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": None,
                "created_at":row['chefs.created_at'],
                "updated_at": row['chefs.updated_at']                
            }
            chef_obj = chef.Chef(chef_data)
            one_recipe.maker = chef_obj
            all_recipes.append(one_recipe)
        return all_recipes


    @classmethod
    def get_one_with_chef(cls, data):
        query = "SELECT * FROM recipes JOIN chefs ON chefs.id = recipes.chef_id WHERE recipes.id = %(id)s;" 
        results = connectToMySQL('recipes_core').query_db(query, data)
        print(results)
        for row in results:
            one_recipe = cls(row)
            print('printing one recipe from model', one_recipe)
            chef_data = {
                "id": row['chefs.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": None,
                "created_at":row['chefs.created_at'],
                "updated_at": row['chefs.updated_at']  
            }
            print('printing chef data from models', chef_data)
            chef_obj = chef.Chef(chef_data)
            one_recipe.maker = chef_obj
            print(one_recipe.maker)
        return one_recipe


    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 1:
            flash("*Recipe requires a name")
            is_valid = False  
        if len(recipe['description']) < 2:
            flash("*Please add recipe description")
            is_valid = False    
        if len(recipe['instructions']) < 2:
            flash("*Recipe requires instructions")
            is_valid = False
        if len(recipe['date_made']) <=0:
            flash("*Please add a date")
            is_valid = False
        if len(recipe['cooking_time']) <2:
            flash("*Please add if cooking time is more or less than 30 minutes")
            is_valid = False   
        return is_valid        


