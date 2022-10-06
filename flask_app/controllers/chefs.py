from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models.chef import Chef
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def home_page():
    return render_template("home_page.html")


@app.route('/welcome')
def welcome_chef():
    if "chef_id" not in session:
        return redirect('/')
    data = {
        "id": session['chef_id']
    }
    return render_template("welcome_page.html", logged_in_chef = Chef.get_by_id(data), all_the_recipes = Recipe.get_all_with_chefs())


#Register-----------------------------------------------------------------------------------------------------------


@app.route('/register', methods=["POST"])
def register_chef():
    print(request.form)
    if not Chef.validate_create(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])    
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash  
    }
    chef_id = Chef.register_chef(data)
    session['chef_id'] = chef_id
    return redirect('/welcome') 



#Login and Logout----------------------------------------------------------------------------------------------------


@app.route('/login', methods=["POST"])
def login_chef():
    print(request.form)
    data = {
        "email": request.form['email']
    }
    chef_in_db = Chef.get_by_email(data)
    if not chef_in_db:
        flash("*The email or password is incorrect")
        return redirect('/')
    if not bcrypt.check_password_hash(chef_in_db.password, request.form['password']):
        flash("*The email or password is incorrect")
        return redirect('/')
    session['chef_id'] = chef_in_db.id
    return redirect('/welcome')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')            




