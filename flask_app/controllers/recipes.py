from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models.recipe import Recipe
from flask_app.models.chef import Chef
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/add_recipe')
def add_recipe():
    
    return render_template("add_recipe.html")


@app.route('/submit_recipe', methods = ["POST"])
def create_recipe():
    if "chef_id" not in session:
        return redirect("/")
    if not Recipe.validate_recipe(request.form):
        return redirect('/add_recipe')    
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "date_made": request.form['date_made'],
        "cooking_time": request.form['cooking_time'],
        "chef_id": session['chef_id']
    }
    Recipe.create(data)
    return redirect("/welcome")


@app.route('/view_recipe/<int:id>')
def view_recipe(id):
    data = {
        "id": id, 
        }
    logged_chef_data = {
        "id": session['chef_id']
    }

    a_recipe = Recipe.get_one_with_chef(data)
    a_chef = Chef.get_by_id(logged_chef_data)
    return render_template("view_recipe.html", the_recipe = a_recipe, logged_in_chef = a_chef)


@app.route('/edit_recipe/<int:id>')
def edit_recipe(id):
    data = {
        "id": id
    }
    a_recipe = Recipe.get_recipe(data)
    return render_template("edit_recipe.html", the_recipe = a_recipe)



@app.route('/delete_recipe/<int:id>', methods=["POST"])
def delete_recipe(id):
    data = {
        "id": id
    }
    Recipe.delete(data)
    return redirect('/welcome')



@app.route('/update_recipe/<int:id>', methods=["POST"])
def update_recipe(id):
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/edit_recipe/{id}')
    data ={
        "id": id,
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "date_made": request.form['date_made'],
        "cooking_time": request.form['cooking_time'],
        "chef_id": session['chef_id']
    }
    Recipe.update(data)
    return redirect(f'/view_recipe/{id}')     