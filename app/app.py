from flask import Flask, jsonify, request
import json
import csv
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, Union, List

app = Flask(__name__)

csv_file_path: str = 'reservations.csv'
csv_encoding: str = 'utf-8'
json_file_path: str = 'hotel_information.json'

# Load hotel information from JSON
with open(json_file_path, 'r') as json_file:
    hotel_info: Dict[str, int] = json.load(json_file)['inventory']

# Load reservations from CSV
@dataclass
class Reservation:
    reservation_id: str
    room_id: str
    hotel_id: str
    guest_name: str
    arrival_date: str
    nights: int
    room_count: int

reservations: List[Reservation] = []
with open(csv_file_path, 'r', encoding=csv_encoding) as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        reservations.append(Reservation(
            reservation_id=row['reservation_id'],
            room_id=row['room_id'],
            hotel_id=row['hotel_id'],
            guest_name=row['guest_name'],
            arrival_date=row['arrival_date'],
            nights=int(row['nights']),
            room_count=int(row['room_count'])
        ))

def get_overlap_dates(start_date: str, nights: int) -> List[datetime]:
    start_date = datetime.strptime(start_date.split()[0], '%Y-%m-%d')
    end_date = start_date + timedelta(days=nights)
    return [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

def get_availability(reservation_id: str) -> Dict[str, int]:
    # Get reservation details
    for reservation in reservations:
        if reservation.reservation_id == reservation_id:
            room_id = reservation.room_id
            arrival_date = reservation.arrival_date
            nights = reservation.nights
            break
    else:
        return jsonify(message="Reservation not found"), 404

    # Calculate overlapping dates
    overlap_dates = get_overlap_dates(arrival_date, nights)

    # Calculate available rooms
    available_rooms = {room: hotel_info[room] for room in hotel_info}
    for other_reservation in reservations:
        other_start_date = other_reservation.arrival_date
        other_nights = other_reservation.nights
        other_dates = get_overlap_dates(other_start_date, other_nights)

        if any(date in other_dates for date in overlap_dates):
            available_rooms[other_reservation.room_id] -= min(other_reservation.room_count, available_rooms[other_reservation.room_id])

    return {room: max(0, available_rooms[room]) for room in available_rooms}

# Routes
@app.route('/get_reservation', methods=['GET'])
def get_reservation():
    reservation_id = request.args.get('reservation_id')
    if not reservation_id:
        return jsonify(message="Reservation ID is required"), 400

    for reservation in reservations:
        if reservation.reservation_id == reservation_id:
            return jsonify(reservation.__dict__)

    return jsonify(message="Reservation not found"), 404

@app.route('/get_availability', methods=['GET'])
def availability():
    reservation_id = request.args.get('reservation_id')
    if not reservation_id:
        return jsonify(message="Reservation ID is required"), 400

    return jsonify(get_availability(reservation_id))

if __name__ == '__main__':
    app.run(debug=True)
