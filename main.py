# Student ID: 010924345
# Name: Austin Waterman
# Course: C950 Data Structures and Algorithms II
import datetime
from packages import Package
from data import *
from hashtable import ChainingHashTable
from truck import Truck

#Create the three trucks as truck objects, with departure times
truck1 = Truck(1, [], datetime.timedelta(hours=8, minutes=0, seconds=0))
truck2 = Truck(2, [], datetime.timedelta(hours=9, minutes=5, seconds=0))
truck3 = Truck(3, [], datetime.timedelta(hours=10, minutes=20, seconds=0))

#initialize hash table
hash_table = ChainingHashTable()

# Use for loop to call insert function of hashtable and insert each package object, with package ID as the key
for i in range(1, 41):
    var_name = f"pkg{i}"
    hash_table.insert(i, globals()[var_name])

# finds distance between two addresses using lookup table, which is a symmetrical 2D matrix
#Complexity O(1)
def distanceBetween(address1, address2):
    index1 = addressData.index(address1)
    index2 = addressData.index(address2)
    return distanceData[index1][index2]

#Predetermined lists of package IDs to ensure special requirements are met. Algorithmically loading trucks is not a requirement of this assessment.
truck1_packages = [14,15,16,13,19,20,1,29,30,31,34,37,40,27,39,35]
truck2_packages = [18,36,38,6,25,28,32,3,33]
truck3_packages = [9,2,4,5,7,8,10,11,12,17,19,21,22,23,24,26]

#Finds the minimum distance between a specified address and all the packages remaining on the truck
# Complexity - O(n)
def minDistance(fromAddress, truckPackages):
    min = 1000
    nextAddress = ""
    #loop through all packages on the truck
    for package in truckPackages:
        #get distance from current address to the package delivery address
        distance = distanceBetween(fromAddress, package.address)
        #if the distance is smaller than the current minimum, set that delivery address as the next address to visit
        if distance < min:
            min = distance
            nextAddress = package.address

    return nextAddress

# Complexity - O(n)
def loadTruckPackages(truck, deliveries):
    #find package in hashtable, add to packages array in the truck object, and update the package status
    #this function is only called when the truck departs so status is now "en route"
    for pkg in deliveries:
        package = hash_table.search(pkg)
        truck.packages.append(package)
        package.status = "en Route"
        package.departure_time = truck.departure_time

# This function is basically the nearest neighbor algorithm.
# it looks at the current address and moves to the next closest address from the list of all addresses not visited
# Complexity - O(n^3)
def truckDeliverPackages(truck, truck_packages):
    #load packages onto the truck and set status to en route
    loadTruckPackages(truck, truck_packages)
    #initialize path for nearset neighbor delivery algorithm
    path = []
    #create datetime object for 10:20 AM
    ten_twenty = datetime.timedelta(hours=10, minutes=20, seconds=0)
    # Complexity - O(n^3)
    while truck.packages:
        #check if the current time is after 10:20 AM
        if truck.departure_time > ten_twenty:
            package9 = hash_table.search(9)
            #check to see if the address for package 9 has been updated. If not, then update it
            if package9.address == "300 State St":
                package9.address = "410 S State St"
                package9.zip = "84111"

        #find next stop by utilizing nearest neighbor algorithm
        nextStop = minDistance(truck.current_location, truck.packages)

        distance = distanceBetween(truck.current_location, nextStop)
        #add distance between the current stop and the next stop to the trucks mileage
        truck.mileage += distance
        timeToDeliver = distance / 18

        #break down the time to deliver into exact hours, minutes, and seconds
        hours = int(timeToDeliver)
        minutes = int((timeToDeliver * 60) % 60)
        seconds = int((timeToDeliver * 3600) % 60)

        #add the time it will take to deliver this package to the time the truck departed
        delta = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
        truck.departure_time += delta

        #when package is delivered, update status and remove the package from the truck
        # Complexity - O(n^2) worst case
        for pkg in truck.packages:
            if pkg.address == nextStop:
                hash_table.updateStatus(pkg.ID, f"Delivered at: {truck.departure_time}")
                truck.packages.remove(pkg)
                package = hash_table.search(pkg.ID)
                package.delivery_time = truck.departure_time

        # set the currentstop to the location of the next stop after packages have been delivered
        truck.current_location = nextStop
        path.append(nextStop)

    #return to hub
    hub_distance = distanceBetween(path[len(path) - 1], truck.hub_location)
    truck.mileage += hub_distance


class Main:

    #run delivery algorithm at program start
    truckDeliverPackages(truck1, truck1_packages)
    truckDeliverPackages(truck2, truck2_packages)
    truckDeliverPackages(truck3, truck3_packages)

    exit = False
    print("Welcome to the WGUPS Delivery Program.")

    #main loop for user interface
    while not exit:
        #input options
        print("Input Options:")
        print("[m] - return total mileage for all trucks.")
        print("[s] - status for a single packge at specified time")
        print("[a] - status for all packages at specified time")
        print("[q] - exit program")

        #massive try/catch for all inputs
        try:
            usr_input = input(">")
            if usr_input == "m" or usr_input == "M":
                try:
                    #add up mileage from all trucks and print
                    total_mileage = round(truck1.mileage + truck2.mileage + truck3.mileage, 4)
                    print(f"Total Miles Driven: {total_mileage}")

                except:
                    print("Input was invalid, please try again")
            elif usr_input == "s" or usr_input == "S":
                try:
                    input_time = input("Please enter desired time with format HH:MM:SS:")
                    #split up input string using colon as the delimiter
                    (h, m, s) = input_time.split(":")
                    #cast all inputs to int and create datetime object for user inputted time
                    delta = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                    #create datetime object for 10:20 AM
                    ten_twenty = datetime.timedelta(hours=10, minutes=20, seconds=0)
                    #if time is before 10:20 AM, make sure package 9 contains old address
                    if delta < ten_twenty:
                        package9 = hash_table.search(9)
                        package9.update_address("300 State St", "84013")
                    #if time is after 10:20 AM, update package 9 address to correct address
                    if delta >= ten_twenty:
                        package9 = hash_table.search(9)
                        package9.update_address("410 S State St", "84111")
                    input_ID = int(input("Please enter the package ID: "))
                    #find package in hash table
                    package = hash_table.search(input_ID)
                    #updates the status for the package based on the inputted time
                    package.get_status_from_time(delta)
                    #print package object
                    print(package)

                except:
                    print("Input was invalid, please try again")
            elif usr_input == "a" or usr_input == "A":
                try:
                    input_time = input("Please enter desired time with format HH:MM:SS: ")
                    #same as above, converting input string to datetime object
                    (h, m, s) = input_time.split(":")
                    delta = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                    #create datetime object for 10:20 AM
                    ten_twenty = datetime.timedelta(hours=10, minutes=20, seconds=0)
                    #if time is before 10:20 AM, make sure package 9 contains old address
                    if delta < ten_twenty:
                        package9 = hash_table.search(9)
                        package9.update_address("300 State St", "84013")
                    #if time is after 10:20 AM, update package 9 address to correct address
                    if delta >= ten_twenty:
                        package9 = hash_table.search(9)
                        package9.update_address("410 S State St", "84111")
                    #print out all the packages based on what truck they were loaded onto
                    # Complexity - O(n)
                    print("Truck 1: ")
                    for p in truck1_packages:
                        package = hash_table.search(p)
                        package.get_status_from_time(delta)
                        print(package)
                    print("Truck 2: ")
                    for pID in truck2_packages:
                        package = hash_table.search(pID)
                        package.get_status_from_time(delta)
                        print(package)
                    print("Truck 3: ")
                    for pID in truck3_packages:
                        package = hash_table.search(pID)
                        package.get_status_from_time(delta)
                        print(package)

                except:
                    print("Input was invalid, please try again")

            elif usr_input == "q" or usr_input == "Q":
                try:
                    #exit program
                    print("Goodbye :)")
                    exit = True
                except:
                    print("Input was invalid, please try again")

            else:
                print("Input was invalid, please try again")

        except:
            print("Input was invalid, please try again")






