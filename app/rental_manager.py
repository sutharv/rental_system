import json
from datetime import datetime
from models import RentalObject, Bike, Car, RentalEncoder
from customer import Customer

class RentalManager:
    """Manages rental operations, customers, and items"""
    
    def __init__(self):
        self._items = {}
        self._customers = {}
        self._active_rentals = {}  # Track active rentals with (customer_id, item_id) as key
        self._rental_history = []  # Track all rental history

    @property
    def items(self):
        """Get all rental items"""
        return self._items.copy()  # Return copy to prevent direct modification

    @property
    def customers(self):
        """Get all customers"""
        return self._customers.copy()  # Return copy to prevent direct modification

    @property
    def rental_history(self):
        """Get rental history"""
        return self._rental_history.copy()  # Return copy to prevent direct modification

    def add_item(self, item):
        """Add a rental item to the system"""
        if not isinstance(item, RentalObject):
            raise TypeError("Item must be a RentalObject")
        if item.id in self._items:
            raise ValueError(f"Item with ID {item.id} already exists")
        self._items[item.id] = item

    def remove_item(self, item_id):
        """Remove an item from the system"""
        item = self._items.get(item_id)
        if not item:
            raise ValueError(f"Item with ID {item_id} does not exist")
        if item.is_rented:
            raise ValueError("Cannot remove item while it is being rented")
        del self._items[item_id]
        return True

    def add_customer(self, customer):
        """Add a new customer to the system"""
        if not isinstance(customer, Customer):
            raise TypeError("Customer must be a Customer object")
        if customer.id in self._customers:
            raise ValueError(f"Customer with ID {customer.id} already exists")
        self._customers[customer.id] = customer

    def remove_customer(self, customer_id):
        """Remove a customer from the system"""
        customer = self._customers.get(customer_id)
        if not customer:
            raise ValueError(f"Customer with ID {customer_id} does not exist")
        if customer.has_active_rentals():
            raise ValueError("Cannot remove customer while they have active rentals")
        del self._customers[customer_id]
        return True

    def edit_customer(self, customer_id, first_name=None, last_name=None, address=None, contact_number=None):
        """Edit customer details"""
        customer = self._customers.get(customer_id)
        if not customer:
            raise ValueError(f"Customer with ID {customer_id} does not exist")
        customer.edit_details(first_name, last_name, address, contact_number)
        return True

    def rent_item(self, customer_id, item_id):
        """Rent an item to a customer"""
        customer = self._customers.get(customer_id)
        if not customer:
            raise ValueError("Invalid customer ID")
        
        item = self._items.get(item_id)
        if not item:
            raise ValueError("Invalid item ID")

        # These will raise ValueError if there are issues
        item.rent()
        customer.add_rental(item)
        
        self._active_rentals[(customer_id, item_id)] = {
            'start_time': datetime.now(),
            'item': item,
            'customer': customer
        }
        self.save_data()  # Save after successful rental
        return True

    def return_item(self, customer_id, item_id):
        """Return an item rented by a customer"""
        if (customer_id, item_id) not in self._active_rentals:
            raise ValueError("No active rental found for this customer and item")

        customer = self._customers[customer_id]
        item = self._items[item_id]
        
        rental_cost = item.return_item()  # This will raise ValueError if there are issues
        customer.remove_rental(item)
        
        rental_data = self._active_rentals.pop((customer_id, item_id))
        
        # Add to rental history
        history_entry = {
            'customer_id': customer_id,
            'customer_name': customer.get_full_name(),
            'item_id': item_id,
            'item_name': item.name,
            'start_time': rental_data['start_time'].isoformat(),
            'end_time': datetime.now().isoformat(),
            'cost': rental_cost
        }
        self._rental_history.append(history_entry)
        self.save_data()  # Save after successful return
        return rental_cost

    def get_customer_rentals(self, customer_id):
        """Get all active rentals for a customer"""
        if customer_id not in self._customers:
            raise ValueError("Invalid customer ID")
        return [rental for (cid, _), rental in self._active_rentals.items() 
                if cid == customer_id]

    def get_item_rental_history(self, item_id):
        """Get rental history for a specific item"""
        if item_id not in self._items:
            raise ValueError("Invalid item ID")
        return [entry for entry in self._rental_history 
                if entry['item_id'] == item_id]

    def get_customer_rental_history(self, customer_id):
        """Get rental history for a specific customer"""
        if customer_id not in self._customers:
            raise ValueError("Invalid customer ID")
        return [entry for entry in self._rental_history 
                if entry['customer_id'] == customer_id]

    def search_items(self, query):
        """Search items by name, type, or price range"""
        if not query:
            return list(self._items.values())
            
        query = query.lower()
        results = []
        
        try:
            # Try to parse price from query (e.g., "under 50", "over 100")
            if "under" in query or "below" in query:
                price_limit = float(''.join(filter(str.isdigit, query)))
                results.extend([item for item in self._items.values() 
                              if item.rental_price <= price_limit])
            elif "over" in query or "above" in query:
                price_limit = float(''.join(filter(str.isdigit, query)))
                results.extend([item for item in self._items.values() 
                              if item.rental_price >= price_limit])
            else:
                # Search by name or type
                for item in self._items.values():
                    type_info = item.get_type_info()
                    if (query in item.name.lower() or
                        query in type_info.get('bike_type', '').lower() or
                        query in type_info.get('brand', '').lower()):
                        results.append(item)
        except:
            # If price parsing fails, just search by name
            results = [item for item in self._items.values() 
                      if query in item.name.lower()]
        
        return results

    def search_customers(self, query):
        """Search customers by name, address, or contact number"""
        if not query:
            return list(self._customers.values())
            
        query = query.lower()
        return [customer for customer in self._customers.values() 
                if (query in customer.first_name.lower() or
                    query in customer.last_name.lower() or
                    query in customer.address.lower() or
                    query in customer.contact_number.lower() or
                    query in customer.get_full_name().lower())]

    def get_rented_items(self):
        """Get list of currently rented items"""
        return [item for item in self._items.values() if item.is_rented]

    def get_available_items(self):
        """Get list of available (not rented) items"""
        return [item for item in self._items.values() if not item.is_rented]

    def get_customers_with_active_rentals(self):
        """Get list of customers who have active rentals"""
        return [customer for customer in self._customers.values() 
                if customer.has_active_rentals()]

    def save_data(self, filename='data.json'):
        """Save rental items, customers, and history to a JSON file"""
        data = {
            'items': self._items,
            'customers': {cid: customer.to_dict() for cid, customer in self._customers.items()},
            'rental_history': self._rental_history
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4, cls=RentalEncoder)
        except Exception as e:
            print(f"Error saving data: {str(e)}")
            raise

    def load_data(self, filename='data.json'):
        """Load rental items, customers, and history from a JSON file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                
                # Load items
                self._items.clear()
                for item_id, item_data in data['items'].items():
                    item_type = item_data.get('type', 'generic')
                    if item_type == 'bike':
                        self._items[item_id] = Bike.from_dict(item_data)
                    elif item_type == 'car':
                        self._items[item_id] = Car.from_dict(item_data)
                
                # Load customers
                self._customers = {
                    customer_id: Customer.from_dict(customer_data) 
                    for customer_id, customer_data in data['customers'].items()
                }
                
                # Load rental history
                self._rental_history = data.get('rental_history', [])
                
                # Reconstruct active rentals from item status
                self._active_rentals.clear()
                for item_id, item in self._items.items():
                    if item.is_rented:
                        for customer in self._customers.values():
                            if item in customer.active_rentals:
                                self._active_rentals[(customer.id, item_id)] = {
                                    'start_time': datetime.fromisoformat(item._current_rental_start) if item._current_rental_start else datetime.now(),
                                    'item': item,
                                    'customer': customer
                                }
                                break
                
        except FileNotFoundError:
            print("Data file not found. Starting with empty data.")
        except json.JSONDecodeError:
            print("Error reading data file. Starting with empty data.")
        except Exception as e:
            print(f"Error loading data: {str(e)}. Starting with empty data.")
            raise
