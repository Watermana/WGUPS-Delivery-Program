# packages file

class Package:
    def __init__(self, ID, address, deadline, city, zip, weight, note="none", status="at hub"):

        self.ID = ID
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip = zip
        self.weight = weight
        self.note = note
        self.status = status
        self.departure_time = None
        self.delivery_time = None

    def get_status_from_time(self, input_time):
        if input_time < self.departure_time:
            self.status = "At hub"
        elif input_time < self.delivery_time:
            self.status = "En route"

    def update_address(self, new_address, new_zip, new_city="Salt Lake City"):
        self.address = new_address
        self.city = new_city
        self.zip = new_zip


    def __str__(self):

        return (f"Package [ID: {self.ID}, Address: {self.address}, Deadline: {self.deadline}, City: {self.city}, "
                f"Zip Code: {self.zip}, Weight: {self.weight}, Status: {self.status}, Special Notes: {self.note}]")

