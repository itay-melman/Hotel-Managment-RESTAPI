# Hotel Reservation API

This Flask application provides a simple API for managing hotel reservations. 
It includes two endpoints:

1. **Get Reservation**
   - **Endpoint:** `/get_reservation`
   - **Method:** GET
   - **Parameters:** `reservation_id` (string)
   - **Description:** Retrieves details for a specific reservation based on the provided `reservation_id` according to the data in reservations.csv

2. **Get Availability**
   - **Endpoint:** `/get_availability`
   - **Method:** GET
   - **Parameters:** `reservation_id` (string)
   - **Description:** Determines the availability of rooms in the hotel for the dates specified in the reservation according to the data in reservations.csv and hotel_information.json

**run the app:**
python app.py

**Usage:**
curl -X GET "http://127.0.0.1:5000/get_reservation?reservation_id=your_reservation_id"

curl -X GET "http://127.0.0.1:5000/get_availability?reservation_id=your_reservation_id"

