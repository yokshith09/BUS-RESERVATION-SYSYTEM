# 🚌 Bus Reservation System  

## 📌 Project Overview  
This project is a **Bus Reservation System** implemented in **Python** using **Data Structures and Algorithms (DSA)** concepts such as **Linked List, Queue, and Stack**.  
It allows users to search buses, reserve seats, confirm tickets, cancel reservations, and view express buses.  

The system simulates a real-world bus booking system and demonstrates the application of **DSA in software design**.  

---

## ⚙️ Features  
- **Display All Buses** → Shows a list of available buses with details.  
- **Search Buses** → Search buses based on **boarding city, destination city, and travel date**.  
- **Seat Reservation** → Book seats with passenger details and get a unique **PIN**.  
- **Confirm Ticket** → Verify reservations using the confirmation PIN and process payment.  
- **Express Buses** → View available **Express category** buses.  
- **Cancel Ticket** → Cancel booked tickets using the confirmation PIN.  
- **File Handling** → Generates a `ticket_confirmation.txt` file for confirmed tickets.  

---

## 🧑‍💻 Data Structures Used  
- **Linked List** → To store and manage all available buses.  
- **Queue (Deque)** → Used for the waiting queue (future expansion).  
- **Stack** → Maintains a history of reserved buses.  
- **2D Array** → Represents seat arrangement (8 rows × 4 seats = 32 seats per bus).  

---

## 📂 Project Structure  
BusReservationSystem/
│── bus_reservation.py # Main program
│── ticket_confirmation.txt # Generated file for confirmed tickets
│── README.md # Documentation


---

## 🚀 How to Run  
1. Make sure you have **Python 3.x** installed.  
2. Clone or download the project.  
3. Open terminal/command prompt in the project directory.  
4. Run the script:  
   ```bash
   python bus_reservation.py

# When you run the program, you’ll see:
Welcome to the Bus Reservation System
1. Display All Buses
2. Search for Buses
3. Reserve a Seat
4. Confirm Ticket
5. Show Express Buses
6. Cancel Ticket
7. Exit

# Learning Outcomes
Implementation of Linked Lists, Stacks, and Queues in a real-world application.
File handling in Python.
Object-Oriented Programming (OOP) design.
Practical understanding of DSA concepts in system design.

# Test Case
<img width="612" height="714" alt="image" src="https://github.com/user-attachments/assets/051a5c1f-1e52-42d2-b56f-5d8f2f68fe8d" />
<img width="612" height="714" alt="image" src="https://github.com/user-attachments/assets/5d470ee0-e462-458c-9bbe-b39f5f025c10" />
<img width="870" height="714" alt="image" src="https://github.com/user-attachments/assets/9101fa4c-c792-4735-94c7-43b04776f8df" />
<img width="690" height="573" alt="image" src="https://github.com/user-attachments/assets/3858b027-756a-4203-ad6d-b1aeca79384f" />
**Confirmed Ticket**
<img width="612" height="714" alt="image" src="https://github.com/user-attachments/assets/99128e10-39f0-4396-8dd4-dbf0e4b57403" />
