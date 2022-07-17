from app import app
from flask import Flask, render_template, redirect, session, request
from flask_bcrypt import Bcrypt
from app.models.user import User
from app.models.listing import Listing

@app.route('/dashboard')
def view_dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    all_listings=User.get_all_users_listing()
    print(all_listings)
    return render_template('dashboard.html', user=User.get_one(data), all_listings=all_listings)

# ------ route that render the page to report a sightings for the user. 
@app.route('/dashboard/new/')
def report():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : session['user_id']
    }
    return render_template('new_listing.html', user=User.get_one(data))

#------ hidden route that takes in the listing form, saves and redirects to dashboard.
@app.route('/dashboard/new/create', methods=['POST'])
def create():
    is_valid = Listing.validate(request.form)
    if not is_valid:
        return redirect('/dashboard/new/')
    data = {
        'property_name': request.form['property_name'],
        'property_type': request.form['property_type'],
        'address' : request.form['address'],
        'year_built': request.form ['year_built'],
        'price': request.form ['price'],
        'image': request.form['image'],
        'description': request.form['description'],
        'number_of_bedrooms': request.form['number_of_bedrooms'],
        'number_of_bathrooms': request.form['number_of_bathrooms'],
        'users_id':request.form ['users_id']
    }
    Listing.save(data)
    return redirect('/dashboard')

#------ app route that deletes a car.
@app.route('/dashboard/delete/<int:id>')
def delete_car(id):
    data = {
        'id': id
    }
    Listing.delete(data)
    return redirect('/dashboard')

#----- app route that takes to view details. 
@app.route('/dashboard/show/<int:id>')
def show_details(id):
    data = {
        'id':id
    }
    return render_template('show_details.html', user=User.get_one({'id': session['user_id']}), one_listing=Listing.get_oneW_user(data))

#----- app routes that renders the edit.
@app.route('/dashboard/edit/<int:id>')
def edit(id):
    data ={
    'id':id
    }
    return render_template('edit_listing.html', user=User.get_one(data), one_listing=Listing.get_one(data))

#----- app route that updates & redirects back to the dashboard. 
@app.route('/dashboard/edit/update/<int:id>', methods=['POST'])
def update(id):
    # is_valid = Listing.validate(request.form)
    # if not is_valid:
    #     return redirect('/dashboard/edit/<int:id>')
    data = {
        'property_name': request.form['property_name'],
        'address': request.form['address'],
        'price':request.form['price'],
        'description': request.form['description'],
        'id':id
    }
    Listing.update(data)
    return redirect('/dashboard')

