class Truck:
    def __init__(self, truckID, packages, departure_time, mileage=0 ):

        self.truckID = truckID
        self.packages = packages
        self.mileage = mileage
        self.hub_location = "4001 South 700 East"
        self.current_location = self.hub_location
        self.departure_time = departure_time
