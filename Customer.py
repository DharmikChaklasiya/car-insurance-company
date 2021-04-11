import uuid
# Represents the customer of the car insurance company
class Customer:
    def __init__(self, name, address):
        self.ID= str(uuid.uuid1())
        self.name = name
        self.address = address
        self.cars = [] # List of cars

    def addCar (self, car):
        self.cars.append(car)

    # convert object o JSON
    def serialize(self):
        car_detail = [[car.model_name,car.number_plate,car.motor_power,car.year] for car in self.cars]

        return {
            'id': self.ID, 
            'name': self.name, 
            'address': self.address,
            'cars': car_detail
        }
    
class Car :
    def __init__(self, model_name, number_plate, motor_power, year):
        self.model_name = model_name
        self.number_plate = number_plate
        self.motor_power = motor_power
        self.year = year