import random
from collections import deque
from datetime import datetime, timedelta
import os

class BusNode:
    def __init__(self, bus):
        self.bus = bus
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
        self.express = express
        self.seats = [["Empty" for _ in range(4)] for _ in range(8)]
        self.reserved_info = []

    def reserve_seat(self):
        if all(seat != "Empty" for row in self.seats for seat in row):
            print("Bus is full. Please wait for the next bus.")
            return

        self.display_seats()
        try:
            number_of_tickets = int(input("How many tickets do you want to book? "))
            if number_of_tickets < 1:
                print("You must book at least one ticket.")
                return

            available_seats = sum(seat == "Empty" for row in self.seats for seat in row)
            if number_of_tickets > available_seats:
                print(f"Only {available_seats} seat(s) available. Cannot book {number_of_tickets} tickets.")
                return

            pin = self.generate_pin()
            print(f"Your confirmation PIN for all tickets is: {pin}")

            total_cost = 0

            for _ in range(number_of_tickets):
                seat_number = int(input("Enter Seat Number (1-32): "))
                if seat_number < 1 or seat_number > 32:
                    print("Invalid Seat Number! There are only 32 seats.")
                    return

                row, col = (seat_number - 1) // 4, (seat_number - 1) % 4
                if self.seats[row][col] == "Empty":
                    name = input("Enter Passenger's Name: ")
                    age = input("Enter Passenger's Age: ")
                    gender = input("Enter Passenger's Gender: ")
                    mobile = input("Enter Passenger's Mobile Number: ")

                    self.seats[row][col] = "Confirmed"
                    self.reserved_info.append({
                        "name": name,
                        "age": age,
                        "gender": gender,
                        "mobile": mobile,
                        "seat_number": seat_number,
                        "pin": pin
                    })
                    print(f"Seat number {seat_number} has been reserved for {name}.")
                    total_cost += self.fare
                else:
                    print(f"Seat {seat_number} is already reserved. Please select another.")

            print(f"\nTotal fare for {number_of_tickets} tickets is: ${total_cost:.2f}")

        except ValueError:
            print("Invalid input. Please enter a valid seat number.")

    def display_seats(self):
        print(f"\nSeats for Bus {self.bus_number}:")
        seat_num = 1
        for row in self.seats:
            row_display = []
            for seat in row:
                status = "Confirmed" if seat != "Empty" else "Empty"
                row_display.append(f"Seat {seat_num}: {status}")
                seat_num += 1
            print(" | ".join(row_display))

    def generate_pin(self):
        return random.randint(1000, 9999)

class BusReservationSystem:
    def __init__(self):
        self.buses = BusLinkedList()
        self.waiting_queue = deque()
        self.reserved_stack = []
        self.predefined_buses()

    def predefined_buses(self):
        start_date = datetime.now()
        cities = ["Coimbatore", "Pallakkad", "Ettimadai", "Podanur"]
        timings = [("10:00 AM", "11:00 AM"), ("12:00 PM", "1:00 PM"),
                   ("2:00 PM", "3:00 PM"), ("4:00 PM", "5:00 PM")]
        drivers = ["John Doe", "Jane Smith", "Jim Brown", "Emily Davis"]
        fares = [20.0, 25.0, 30.0, 35.0]

        for day in range(7):
            travel_date = (start_date + timedelta(days=day)).strftime('%Y-%m-%d')
            for from_city in cities:
                for to_city in cities:
                    if from_city != to_city:
                        for j, (dep, arr) in enumerate(timings):
                            bus_number = f"{from_city[0]}{to_city[0]}{random.randint(100, 999)}"
                            driver = drivers[j % len(drivers)]
                            fare = fares[j % len(fares)]
                            express = random.choice([True, False])
                            bus = Bus(bus_number, driver, arr, dep, from_city, to_city, fare, travel_date, express)
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
            self.reserved_stack.append(bus_number)
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
            try:
                pin = int(input("Enter your confirmation PIN: "))
                reservations = [r for r in bus.reserved_info if r['pin'] == pin]
                if reservations:
                    total_fare = len(reservations) * bus.fare
                    print(f"The total fare for {len(reservations)} tickets is: ${total_fare:.2f}")
                    payment_amount = float(input("Enter payment amount: $"))

                    if payment_amount >= total_fare:
                        print(f"Payment of ${payment_amount:.2f} successful!")
                        with open("ticket_confirmation.txt", "w") as file:
                            file.write("Your ticket is confirmed!\n")
                            for res in reservations:
                                file.write(f"Passenger: {res['name']}, Seat: {res['seat_number']}, Mobile: {res['mobile']}\n")
                        os.startfile("ticket_confirmation.txt")
                        return
                    else:
                        print("Insufficient payment.")
                else:
                    print("Invalid PIN.")
            except ValueError:
                print("Invalid input.")
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
            try:
                pin = int(input("Enter your confirmation PIN: "))
                cancelled = [r for r in bus.reserved_info if r['pin'] == pin]
                if cancelled:
                    for res in cancelled:
                        seat_number = res['seat_number']
                        row, col = (seat_number - 1) // 4, (seat_number - 1) % 4
                        bus.seats[row][col] = "Empty"
                    bus.reserved_info = [r for r in bus.reserved_info if r['pin'] != pin]
                    print(f"All reservations with PIN {pin} have been cancelled.")
                else:
                    print("No matching reservations found.")
            except ValueError:
                print("Invalid input.")
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
