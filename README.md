# Rental Management System

A Flask-based web application for managing rental items (bikes and cars) and customers. The system follows object-oriented principles and provides a complete solution for rental operations.

## Features

- Item Management (Bikes and Cars)
  - Add, edit, and remove rental items
  - Track item availability
  - View item rental history
  - Search items by name, type, or price range

- Customer Management
  - Add, edit, and remove customers
  - Track customer rentals
  - View customer rental history
  - Search customers by name, contact, or address

- Rental Operations
  - Rent items to customers
  - Return items with automatic cost calculation
  - View rental history
  - Track active rentals

## Project Structure

```
rental_system/
├── app/
│   ├── __init__.py
│   ├── app.py              # Flask application setup
│   ├── routes.py           # URL routes and view functions
│   ├── models.py           # Rental item models (RentalObject, Car, Bike)
│   ├── customer.py         # Customer model
│   ├── rental_manager.py   # Business logic and data management
│   ├── static/             # Static files (CSS, JS)
│   └── templates/          # HTML templates
│       ├── index.html
│       ├── add_item.html
│       ├── add_customer.html
│       ├── edit_customer.html
│       ├── available_items.html
│       ├── customers.html
│       ├── customer_history.html
│       ├── item_history.html
│       └── recent_rental_history.html
├── data.json               # Persistent data storage
└── requirements.txt        # Python dependencies
```

## Class Documentation

### RentalObject (Abstract Base Class)
Base class for all rental items.

**Properties:**
- `id`: Unique identifier
- `name`: Item name
- `rental_price`: Price per hour
- `is_rented`: Current rental status
- `rental_history`: List of past rentals

**Methods:**
- `rent()`: Mark item as rented
- `return_item()`: Return item and calculate cost
- `get_type_info()`: Get type-specific information (abstract)
- `to_dict()`: Convert to dictionary for serialization
- `from_dict()`: Create object from dictionary

### Car (RentalObject)
Represents a rental car.

**Additional Properties:**
- `brand`: Car brand

### Bike (RentalObject)
Represents a rental bike.

**Additional Properties:**
- `bike_type`: Type of bike

### Customer
Represents a customer who can rent items.

**Properties:**
- `id`: Unique identifier
- `first_name`: First name
- `last_name`: Last name
- `address`: Address
- `contact_number`: Contact number
- `active_rentals`: Currently rented items

**Methods:**
- `add_rental()`: Add a rented item
- `remove_rental()`: Remove a returned item
- `has_active_rentals()`: Check for active rentals
- `get_full_name()`: Get customer's full name
- `edit_details()`: Update customer information

### RentalManager
Manages all rental operations and data persistence.

**Properties:**
- `items`: All rental items
- `customers`: All customers
- `rental_history`: Complete rental history

**Methods:**
- Item Management:
  - `add_item()`
  - `remove_item()`
  - `search_items()`
  - `get_available_items()`
  - `get_rented_items()`

- Customer Management:
  - `add_customer()`
  - `remove_customer()`
  - `edit_customer()`
  - `search_customers()`
  - `get_customers_with_active_rentals()`

- Rental Operations:
  - `rent_item()`
  - `return_item()`
  - `get_customer_rentals()`
  - `get_item_rental_history()`
  - `get_customer_rental_history()`

- Data Persistence:
  - `save_data()`
  - `load_data()`

## Object-Oriented Design Principles

1. **Encapsulation**
   - Private attributes with controlled access
   - Input validation in setters
   - Protected collections

2. **Inheritance**
   - Abstract base class for rental items
   - Specialized car and bike classes
   - Common interface implementation

3. **Polymorphism**
   - Type-specific behavior through overridden methods
   - Consistent interfaces across classes
   - Dynamic object creation from data

4. **Object Management**
   - Clear separation of concerns
   - Centralized data management
   - Relationship handling

## Usage Examples

1. Adding a New Car:
```python
car = Car(
    id="1",
    name="Toyota Camry",
    rental_price=50.0,
    brand="Toyota"
)
rental_manager.add_item(car)
```

2. Adding a New Customer:
```python
customer = Customer(
    id="1",
    first_name="John",
    last_name="Doe",
    address="123 Main St",
    contact_number="555-0123"
)
rental_manager.add_customer(customer)
```

3. Renting an Item:
```python
rental_manager.rent_item(
    customer_id="1",
    item_id="1"
)
```

4. Returning an Item:
```python
cost = rental_manager.return_item(
    customer_id="1",
    item_id="1"
)
print(f"Rental cost: ${cost:.2f}")
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sutharv/rental_system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app/app.py
```

4. Open in browser:
```
http://localhost:5000
```

## Data Persistence

The system uses JSON for data persistence:
- Data is automatically saved after each operation
- Data is loaded when the application starts
- All data is stored in `data.json`

## Error Handling

The system includes comprehensive error handling:
- Input validation
- Business rule validation
- Data integrity checks
- Proper error messages
- Exception handling

## Future Enhancements

Possible improvements:
1. Additional rental item types
2. Advanced pricing models
3. Reservation system
4. Payment processing
5. User authentication
6. API endpoints
7. Reports and analytics
8. Email notifications
