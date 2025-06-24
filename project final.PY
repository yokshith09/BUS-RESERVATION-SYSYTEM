import random
from collections import deque
from datetime import datetime, timedelta
import os

class BusNode:
    def __init__(self, bus):
        self.bus = bus  # Stores a Bus object
        self.next = None

class BusLinkedList:
    def __init__(self):
        self.head = None

    def add_bus(self, bus):
        new_node = BusNode(bus)
        if not self.head:
            self.head = new_node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_node

    def find_bus(self, bus_number):
        temp = self.head
        while temp:
            if temp.bus.bus_number == bus_number:
                return temp.bus
            temp = temp.next
        return None

    def search_buses(self, from_city, to_city, travel_date):
        temp = self.head
        found = False
        print(f"Buses from {from_city} to {to_city} on {travel_date}:")
        while temp:
            bus = temp.bus
            if bus.fromCity == from_city and bus.toCity == to_city and bus.date == travel_date:
                found = True
                print(f"Bus Number: {bus.bus_number}, Driver: {bus.driver_name}, "
                      f"Departure Time: {bus.departure_time}, Fare: {bus.fare}")
            temp = temp.next
        if not found:
            print("No buses available for the given route and date.")

class Bus:
    def __init__(self, bus_number, driver_name, arrival_time, departure_time, from_city, to_city, fare, date, express=False):
        self.bus_number = bus_number
        self.driver_name = driver_name
        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.fromCity = from_city
        self.toCity = to_city
        self.fare = fare
        self.date = date
        self.express = express  # Added express flag
        self.seats = [["Empty" for _ in range(4)] for _ in range(8)]  # 32 seats
        self.reserved_info = []  # To store reserved information

    def reserve_seat(self):
        self.display_seats()  # Show booked and available seats before reserving
        try:
            number_of_tickets = int(input("How many tickets do you want to book? "))
            if number_of_tickets < 1:
                print("You must book at least one ticket.")
                return

            # Generate a single PIN for all tickets
            pin = self.generate_pin()
            print(f"Your confirmation PIN for all tickets is: {pin}")  # Display PIN to user
            
            total_cost = 0  # Variable to accumulate total cost

            for _ in range(number_of_tickets):
                seat_number = int(input("Enter Seat Number (1-32): "))
                if seat_number > 32 or seat_number < 1:
                    print("\nInvalid Seat Number! There are only 32 seats.")
                    return
                row, col = (seat_number - 1) // 4, (seat_number - 1) % 4
                if self.seats[row][col] == "Empty":
                    passenger_name = input("Enter Passenger's Name: ")
                    passenger_age = input("Enter Passenger's Age: ")
                    passenger_gender = input("Enter Passenger's Gender: ")
                    passenger_mobile = input("Enter Passenger's Mobile Number: ")

                    # Reserve seat and save passenger information
                    self.seats[row][col] = "Confirmed"  # Show as confirmed
                    # Save passenger information along with the single PIN
                    self.reserved_info.append({
                        "name": passenger_name,
                        "age": passenger_age,
                        "gender": passenger_gender,
                        "mobile": passenger_mobile,
                        "seat_number": seat_number,
                        "pin": pin  # Use the single PIN for all tickets
                    })
                    print(f"Seat number {seat_number} has been reserved for {passenger_name}.")
                    total_cost += self.fare  # Accumulate total fare
                else:
                    print(f"Seat {seat_number} is already reserved. Please select another seat.")

            print(f"\nTotal fare for {number_of_tickets} tickets is: ${total_cost:.2f}")

        except ValueError:
            print("Invalid input. Please enter a valid seat number.")

    def display_seats(self):
        print(f"\nSeats for Bus {self.bus_number}:")
        seat_num = 1
        for row in self.seats:
            row_display = []  # Create a list to hold seat status for the current row
            for seat in row:
                status = "Confirmed" if seat != "Empty" else "Empty"
                row_display.append(f"Seat {seat_num}: {status}")
                seat_num += 1
            print(" | ".join(row_display))  # Join the seat statuses with a separator

    def generate_pin(self):
        """Generate a four-digit confirmation PIN."""
        return random.randint(1000, 9999)

class BusReservationSystem:
    def __init__(self):
        self.buses = BusLinkedList()  # Using linked list to store buses
        self.waiting_queue = deque()  # Queue for waiting passengers
        self.reserved_stack = []  # Stack for recently reserved seats
        self.predefined_buses()  # Predefined buses when the system initializes

    def predefined_buses(self):
        """Add predefined buses for a weekly schedule."""
        start_date = datetime.now()
        cities = ["Coimbatore", "Pallakkad", "Ettimadai", "Podanur"]
        timings = [("10:00 AM", "11:00 AM"), ("12:00 PM", "1:00 PM"), ("2:00 PM", "3:00 PM"), ("4:00 PM", "5:00 PM")]
        drivers = ["John Doe", "Jane Smith", "Jim Brown", "Emily Davis"]
        fares = [20.0, 25.0, 30.0, 35.0]

        for day in range(7):  # Weekly schedule
            travel_date = (start_date + timedelta(days=day)).strftime('%Y-%m-%d')
            for from_city in cities:
                for to_city in cities:
                    if from_city != to_city:  # Prevent a bus from going to the same city
                        for j, (departure_time, arrival_time) in enumerate(timings):
                            bus_number = f"{from_city[0]}{to_city[0]}{random.randint(100, 999)}"
                            driver_name = drivers[j % len(drivers)]
                            fare = fares[j % len(fares)]
                            # Randomly decide if the bus is express
                            express = random.choice([True, False])
                            bus = Bus(bus_number, driver_name, arrival_time, departure_time, from_city, to_city, fare, travel_date, express)
                            self.buses.add_bus(bus)

    def search_buses(self):
        from_city = input("Enter boarding city: ")
        to_city = input("Enter destination city: ")
        travel_date = input("Enter travel date (YYYY-MM-DD): ")
        self.buses.search_buses(from_city, to_city, travel_date)

    def reserve_seat(self):
        bus_number = input("Enter Bus Number: ")
        bus = self.buses.find_bus(bus_number)
        if bus:
            bus.reserve_seat()
            self.reserved_stack.append(bus_number)  # Track reserved buses in stack
        else:
            print("Bus not found.")

    
    def display_buses(self):
        temp = self.buses.head
        if not temp:
            print("No buses available.")
            return

        print("\nAvailable Buses:")
        while temp:
            bus = temp.bus
            express_tag = " (Express)" if bus.express else ""
            print(f"Bus Number: {bus.bus_number}, From: {bus.fromCity}, To: {bus.toCity}, "
                  f"Departure: {bus.departure_time}, Arrival: {bus.arrival_time}, Fare: {bus.fare}, "
                  f"Date: {bus.date}{express_tag}")
            temp = temp.next
            
    def confirm_ticket(self):
        bus_number = input("Enter Bus Number: ")
        bus = self.buses.find_bus(bus_number)
        if bus:
            pin = int(input("Enter your confirmation PIN: "))
            # Collect all reservations for the provided PIN
            reservations = [r for r in bus.reserved_info if r['pin'] == pin]
            
            if reservations:
                # Calculate total fare
                total_fare = len(reservations) * bus.fare
                print(f"The total fare for {len(reservations)} tickets is: ${total_fare:.2f}")

                payment_amount = float(input("Enter payment amount: $"))

                # Simple payment validation
                if payment_amount >= total_fare:
                    print(f"Payment of ${payment_amount:.2f} successful!")
                    
                    # Write ticket details to a text file
                    with open("ticket_confirmation.txt", "w") as file:
                        file.write("Your ticket is confirmed!\n")
                        for reservation in reservations:
                            file.write(f"Passenger Name: {reservation['name']}, Seat Number: {reservation['seat_number']}, Mobile: {reservation['mobile']}\n")


                    # Automatically open the text file
                    os.startfile("ticket_confirmation.txt")

                    return
                else:
                    print("Insufficient payment. Tickets cannot be confirmed.")
                    return
            else:
                print("Invalid PIN. Please try again.")
        else:
            print("Bus not found.")
        

    def show_express_buses(self):
        temp = self.buses.head
        found = False
        print("\nAvailable Express Buses:")
        while temp:
            bus = temp.bus
            if bus.express:
                found = True
                print(f"Bus Number: {bus.bus_number}, From: {bus.fromCity}, To: {bus.toCity}, "
                      f"Departure: {bus.departure_time}, Arrival: {bus.arrival_time}, Fare: {bus.fare}, "
                      f"Date: {bus.date}")
            temp = temp.next
        if not found:
            print("No express buses available.")
    
    def cancel_ticket(self):
        bus_number = input("Enter Bus Number: ")
        bus = self.buses.find_bus(bus_number)
        if bus:
            pin = int(input("Enter your confirmation PIN: "))
            # Find reservations matching the PIN
            cancelled_reservations = [r for r in bus.reserved_info if r['pin'] == pin]
            
            if cancelled_reservations:
                for reservation in cancelled_reservations:
                    seat_number = reservation['seat_number']
                    row, col = (seat_number - 1) // 4, (seat_number - 1) % 4
                    bus.seats[row][col] = "Empty"  # Mark seat as empty
                bus.reserved_info = [r for r in bus.reserved_info if r['pin'] != pin]  # Remove from reserved info
                print(f"All reservations with PIN {pin} have been cancelled.")
            else:
                print("Invalid PIN. No matching reservations found.")
        else:
            print("Bus not found.")

def main():
    system = BusReservationSystem()
    
    while True:
        print("\nWelcome to the Bus Reservation System")
        print("1. Display All Buses")
        print("2. Search for Buses")
        print("3. Reserve a Seat")
        print("4. Confirm Ticket")
        print("5. Show Express Buses")
        print("6. Cancel Ticket")
        print("7. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            system.display_buses()
        elif choice == '2':
            system.search_buses()
        elif choice == '3':
            system.reserve_seat()
        elif choice == '4':
            system.confirm_ticket()
        elif choice == '5':
            system.show_express_buses()
        elif choice == '6':
            system.cancel_ticket()
        elif choice == '7':
            print("Thank you for using the Bus Reservation System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
