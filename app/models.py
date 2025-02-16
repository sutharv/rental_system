from datetime import datetime
import json
from abc import ABC, abstractmethod

class RentalObject(ABC):
    """Abstract base class for rental objects"""
    
    def __init__(self, id, name, rental_price, is_rented=False, rental_history=None):
        self._validate_init_params(id, name, rental_price)
        self._id = id
        self._name = name
        self._rental_price = rental_price
        self._is_rented = is_rented
        self._rental_history = rental_history or []
        self._current_rental_start = None

    def _validate_init_params(self, id, name, rental_price):
        """Validate initialization parameters"""
        if not id:
            raise ValueError("ID cannot be empty")
        if not name:
            raise ValueError("Name cannot be empty")
        if not isinstance(rental_price, (int, float)) or rental_price <= 0:
            raise ValueError("Rental price must be a positive number")

    @property
    def id(self):
        """Get rental object ID"""
        return self._id

    @property
    def name(self):
        """Get rental object name"""
        return self._name

    @property
    def rental_price(self):
        """Get rental price per hour"""
        return self._rental_price

    @property
    def is_rented(self):
        """Check if object is currently rented"""
        return self._is_rented

    @property
    def rental_history(self):
        """Get rental history"""
        return self._rental_history.copy()  # Return copy to prevent direct modification

    def rent(self):
        """Rent the object"""
        if self._is_rented:
            raise ValueError(f"{self._name} is already rented")
        self._is_rented = True
        self._current_rental_start = datetime.now()
        return True

    def return_item(self):
        """Return the rented object and calculate rental cost"""
        if not self._is_rented:
            raise ValueError(f"{self._name} is not currently rented")
        if not self._current_rental_start:
            raise ValueError("Rental start time not recorded")

        rental_duration = (datetime.now() - self._current_rental_start).total_seconds() / 3600  # hours
        rental_cost = self._rental_price * rental_duration

        # Add to rental history
        rental_record = {
            'start_time': self._current_rental_start.isoformat(),
            'end_time': datetime.now().isoformat(),
            'duration_hours': rental_duration,
            'cost': rental_cost
        }
        self._rental_history.append(rental_record)

        # Reset rental state
        self._is_rented = False
        self._current_rental_start = None

        return rental_cost

    @abstractmethod
    def get_type_info(self):
        """Get type-specific information about the rental object"""
        pass

    def to_dict(self):
        """Convert rental object to dictionary for serialization"""
        return {
            'id': self._id,
            'name': self._name,
            'rental_price': self._rental_price,
            'is_rented': self._is_rented,
            'rental_history': self._rental_history,
            'current_rental_start': self._current_rental_start.isoformat() if self._current_rental_start else None,
            'type': self.get_type_info()['type']
        }

    @classmethod
    def from_dict(cls, data):
        """Create rental object from dictionary"""
        obj = cls(
            id=data['id'],
            name=data['name'],
            rental_price=data['rental_price']
        )
        obj._is_rented = data.get('is_rented', False)
        obj._rental_history = data.get('rental_history', [])
        if data.get('current_rental_start'):
            obj._current_rental_start = datetime.fromisoformat(data['current_rental_start'])
        return obj

    def __str__(self):
        """String representation of rental object"""
        status = "rented" if self._is_rented else "available"
        return f"{self._name} ({self.get_type_info()['type']}) - ${self._rental_price}/hour - {status}"

class Car(RentalObject):
    """Car rental object"""
    
    def __init__(self, id, name, rental_price, brand, is_rented=False, rental_history=None):
        super().__init__(id, name, rental_price, is_rented, rental_history)
        if not brand:
            raise ValueError("Brand cannot be empty")
        self._brand = brand

    @property
    def brand(self):
        """Get car brand"""
        return self._brand

    def get_type_info(self):
        """Get car-specific information"""
        return {
            'type': 'car',
            'brand': self._brand
        }

    def to_dict(self):
        """Convert car object to dictionary"""
        data = super().to_dict()
        data['brand'] = self._brand
        return data

    @classmethod
    def from_dict(cls, data):
        """Create car object from dictionary"""
        return cls(
            id=data['id'],
            name=data['name'],
            rental_price=data['rental_price'],
            brand=data['brand'],
            is_rented=data.get('is_rented', False),
            rental_history=data.get('rental_history', [])
        )

class Bike(RentalObject):
    """Bike rental object"""
    
    def __init__(self, id, name, rental_price, bike_type, is_rented=False, rental_history=None):
        super().__init__(id, name, rental_price, is_rented, rental_history)
        if not bike_type:
            raise ValueError("Bike type cannot be empty")
        self._bike_type = bike_type

    @property
    def bike_type(self):
        """Get bike type"""
        return self._bike_type

    def get_type_info(self):
        """Get bike-specific information"""
        return {
            'type': 'bike',
            'bike_type': self._bike_type
        }

    def to_dict(self):
        """Convert bike object to dictionary"""
        data = super().to_dict()
        data['bike_type'] = self._bike_type
        return data

    @classmethod
    def from_dict(cls, data):
        """Create bike object from dictionary"""
        return cls(
            id=data['id'],
            name=data['name'],
            rental_price=data['rental_price'],
            bike_type=data['bike_type'],
            is_rented=data.get('is_rented', False),
            rental_history=data.get('rental_history', [])
        )

class RentalEncoder(json.JSONEncoder):
    """JSON encoder for rental objects"""
    
    def default(self, obj):
        if isinstance(obj, RentalObject):
            return obj.to_dict()
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)
