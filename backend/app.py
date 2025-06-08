from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# In-memory store for room availability. In a real application this would be a
# database table.
available_rooms = []

@app.post('/availability')
def add_availability():
    """Hotels post available rooms here."""
    data = request.get_json()
    if not data or 'hotel' not in data or 'room_id' not in data:
        abort(400, 'hotel and room_id required')
    available_rooms.append({'hotel': data['hotel'], 'room_id': data['room_id']})
    return jsonify({'status': 'added'}), 201


@app.get('/rooms')
def list_rooms():
    """List all currently available rooms."""
    return jsonify({'rooms': available_rooms})


@app.post('/book')
def book_room():
    """Councils book a room by room_id."""
    data = request.get_json()
    if not data or 'room_id' not in data:
        abort(400, 'room_id required')
    for room in available_rooms:
        if room['room_id'] == data['room_id']:
            available_rooms.remove(room)
            return jsonify({'status': 'booked', 'room': room})
    abort(404, 'room not found')

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)
