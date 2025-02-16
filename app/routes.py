from flask import Blueprint, render_template, request, redirect, url_for, flash
from rental_manager import RentalManager
from models import Bike, Car
from customer import Customer

main = Blueprint('main', __name__)
rental_manager = RentalManager()

# Load data when the application starts
rental_manager.load_data()

@main.route('/')
def index():
    item_query = request.args.get('item_search', '')
    customer_query = request.args.get('customer_search', '')
    
    items = rental_manager.search_items(item_query) if item_query else rental_manager.items.values()
    customers = rental_manager.search_customers(customer_query) if customer_query else rental_manager.customers.values()
    
    rental_history = rental_manager.rental_history
    
    return render_template('index.html', 
                         items=items,
                         customers=customers,
                         rental_history=rental_history,
                         item_query=item_query,
                         customer_query=customer_query)

@main.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        try:
            item_id = request.form['id']
            item_name = request.form['name']
            item_price = float(request.form['rental_price'])
            item_type = request.form['type']
            
            if item_type == 'bike':
                new_item = Bike(item_id, item_name, item_price, request.form['bike_type'])
            else:
                new_item = Car(item_id, item_name, item_price, request.form['brand'])
            
            rental_manager.add_item(new_item)
            rental_manager.save_data()
            flash('Item added successfully!', 'success')
            
        except ValueError as e:
            flash(str(e), 'danger')
        except Exception as e:
            flash('An error occurred while adding the item.', 'danger')
            print(f"Error: {str(e)}")
            
        return redirect(url_for('main.index'))
    return render_template('add_item.html')

@main.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        try:
            customer_id = request.form['id']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            address = request.form['address']
            contact_number = request.form['contact_number']
            
            new_customer = Customer(customer_id, first_name, last_name, address, contact_number)
            rental_manager.add_customer(new_customer)
            rental_manager.save_data()
            flash('Customer added successfully!', 'success')
            
        except ValueError as e:
            flash(str(e), 'danger')
        except Exception as e:
            flash('An error occurred while adding the customer.', 'danger')
            print(f"Error: {str(e)}")
            
        return redirect(url_for('main.index'))
    return render_template('add_customer.html')

@main.route('/rent_item', methods=['POST'])
def rent_item():
    try:
        customer_id = request.form['customer_id']
        item_id = request.form['item_id']
        
        if rental_manager.rent_item(customer_id, item_id):
            rental_manager.save_data()
            flash('Item rented successfully!', 'success')
        else:
            flash('Failed to rent item.', 'danger')
            
    except ValueError as e:
        flash(str(e), 'danger')
    except Exception as e:
        flash('An error occurred while renting the item.', 'danger')
        print(f"Error: {str(e)}")
        
    return redirect(url_for('main.index'))

@main.route('/remove_item/<item_id>', methods=['POST'])
def remove_item(item_id):
    try:
        if rental_manager.remove_item(item_id):
            rental_manager.save_data()
            flash('Item removed successfully!', 'success')
        else:
            flash('Failed to remove item.', 'danger')
    except ValueError as e:
        flash(str(e), 'danger')
    except Exception as e:
        flash('An error occurred while removing the item.', 'danger')
        print(f"Error: {str(e)}")
    return redirect(url_for('main.index'))

@main.route('/return_item', methods=['POST'])
def return_item():
    try:
        customer_id = request.form['customer_id']
        item_id = request.form['item_id']
        
        rental_cost = rental_manager.return_item(customer_id, item_id)
        if rental_cost:
            rental_manager.save_data()
            flash(f'Item returned successfully! Rental cost: ${rental_cost:.2f}', 'success')
        else:
            flash('Failed to return item.', 'danger')
            
    except ValueError as e:
        flash(str(e), 'danger')
    except Exception as e:
        flash('An error occurred while returning the item.', 'danger')
        print(f"Error: {str(e)}")
        
    return redirect(url_for('main.index'))

@main.route('/edit_customer/<customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    try:
        customer = rental_manager.customers.get(customer_id)
        if not customer:
            flash('Customer not found.', 'danger')
            return redirect(url_for('main.index'))

        if request.method == 'POST':
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            address = request.form.get('address')
            contact_number = request.form.get('contact_number')
            
            if rental_manager.edit_customer(customer_id, first_name, last_name, address, contact_number):
                rental_manager.save_data()
                flash('Customer details updated successfully!', 'success')
                return redirect(url_for('main.index'))
        
        return render_template('edit_customer.html', customer=customer)
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('main.index'))

@main.route('/remove_customer/<customer_id>', methods=['POST'])
def remove_customer(customer_id):
    try:
        if rental_manager.remove_customer(customer_id):
            rental_manager.save_data()
            flash('Customer removed successfully!', 'success')
        else:
            flash('Failed to remove customer.', 'danger')
    except ValueError as e:
        flash(str(e), 'danger')
    except Exception as e:
        flash('An error occurred while removing the customer.', 'danger')
        print(f"Error: {str(e)}")
    return redirect(url_for('main.index'))

@main.route('/available_items')
def available_items():
    items = rental_manager.get_available_items()
    return render_template('available_items.html', items=items)

@main.route('/customers')
def customers():
    customers = rental_manager.customers.values()
    return render_template('customers.html', customers=customers)

@main.route('/recent_rental_history')
def recent_rental_history():
    recent_history = rental_manager.rental_history[-5:]  # Get the last 5 rentals
    return render_template('recent_rental_history.html', rentals=recent_history)

@main.route('/customer/<customer_id>/history')
def customer_history(customer_id):
    try:
        customer = rental_manager.customers.get(customer_id)
        if not customer:
            flash('Customer not found.', 'danger')
            return redirect(url_for('main.index'))
            
        history = rental_manager.get_customer_rental_history(customer_id)
        return render_template('customer_history.html', 
                            history=history, 
                            customer=customer)
    except ValueError as e:
        flash(str(e), 'danger')
    except Exception as e:
        flash('Error retrieving customer history.', 'danger')
        print(f"Error: {str(e)}")
    return redirect(url_for('main.index'))

@main.route('/item/<item_id>/history')
def item_history(item_id):
    try:
        item = rental_manager.items.get(item_id)
        if not item:
            flash('Item not found.', 'danger')
            return redirect(url_for('main.index'))
            
        history = rental_manager.get_item_rental_history(item_id)
        return render_template('item_history.html', 
                            history=history, 
                            item=item)
    except ValueError as e:
        flash(str(e), 'danger')
    except Exception as e:
        flash('Error retrieving item history.', 'danger')
        print(f"Error: {str(e)}")
    return redirect(url_for('main.index'))
