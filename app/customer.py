from datetime import datetime

class Customer:
    def __init__(self, id, first_name, last_name, address, contact_number, active_rentals=None):
        self._id = id
        self._first_name = first_name
        self._last_name = last_name
        self._address = address
        self._contact_number = contact_number
        self._active_rentals = active_rentals if active_rentals is not None else []

    @property
    def id(self):
        """Get customer ID"""
        return self._id

    @property
    def first_name(self):
        """Get customer's first name"""
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        """Set customer's first name"""
        if not value:
            raise ValueError("First name cannot be empty")
        self._first_name = value

    @property
    def last_name(self):
        """Get customer's last name"""
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        """Set customer's last name"""
        if not value:
            raise ValueError("Last name cannot be empty")
        self._last_name = value

    @property
    def address(self):
        """Get customer's address"""
        return self._address

    @address.setter
    def address(self, value):
        """Set customer's address"""
        if not value:
            raise ValueError("Address cannot be empty")
        self._address = value

    @property
    def contact_number(self):
        """Get customer's contact number"""
        return self._contact_number

    @contact_number.setter
    def contact_number(self, value):
        """Set customer's contact number"""
        if not value:
            raise ValueError("Contact number cannot be empty")
        self._contact_number = value

    @property
    def active_rentals(self):
        """Get customer's active rentals"""
        return self._active_rentals

    def add_rental(self, rental_item):
        """Add a rental item to customer's active rentals"""
        if rental_item in self._active_rentals:
            raise ValueError("Item is already rented by this customer")
        self._active_rentals.append(rental_item)

    def remove_rental(self, rental_item):
        """Remove a rental item from customer's active rentals"""
        if rental_item not in self._active_rentals:
            raise ValueError("Item is not rented by this customer")
        self._active_rentals.remove(rental_item)
        return True

    def has_active_rentals(self):
        """Check if customer has any active rentals"""
        return len(self._active_rentals) > 0

    def get_full_name(self):
        """Return customer's full name"""
        return f"{self._first_name} {self._last_name}"

    def edit_details(self, first_name=None, last_name=None, address=None, contact_number=None):
        """Edit customer details"""
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if address:
            self.address = address
        if contact_number:
            self.contact_number = contact_number

    def to_dict(self):
        """Convert customer object to dictionary for serialization"""
        return {
            'id': self._id,
            'first_name': self._first_name,
            'last_name': self._last_name,
            'address': self._address,
            'contact_number': self._contact_number,
            'active_rentals': []  # Active rentals are handled by RentalManager
        }

    @classmethod
    def from_dict(cls, data):
        """Create customer object from dictionary"""
        return cls(
            id=data['id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            address=data['address'],
            contact_number=data['contact_number'],
            active_rentals=[]  # Active rentals are handled by RentalManager
        )

    def __str__(self):
        """String representation of customer"""
        return f"{self.get_full_name()} (ID: {self._id})"

    def __eq__(self, other):
        """Compare customers by ID"""
        if not isinstance(other, Customer):
            return False
        return self._id == other._id

    def __hash__(self):
        """Hash customer by ID"""
        return hash(self._id)
