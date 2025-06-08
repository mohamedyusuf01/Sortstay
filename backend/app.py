from dataclasses import dataclass, field
from datetime import datetime
import uuid
from flask import Flask, jsonify, request, abort


@dataclass
class Booking:
    id: str
    council_id: str
    hotel: str
    cost: float
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Council:
    id: str
    name: str
    budget_remaining: float
    bookings: list = field(default_factory=list)


COUNCILS = {}
BOOKINGS = {}

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


@app.post('/councils')
def create_council():
    data = request.get_json(force=True)
    if not data or 'name' not in data or 'budget' not in data:
        abort(400, 'name and budget required')
    cid = str(uuid.uuid4())
    council = Council(id=cid, name=data['name'], budget_remaining=float(data['budget']))
    COUNCILS[cid] = council
    return jsonify({'id': cid, 'name': council.name, 'budget_remaining': council.budget_remaining}), 201


@app.get('/councils/<council_id>/budget')
def council_budget(council_id):
    council = COUNCILS.get(council_id)
    if not council:
        abort(404)
    return jsonify({
        'id': council.id,
        'name': council.name,
        'budget_remaining': council.budget_remaining,
        'bookings': [b.__dict__ for b in council.bookings]
    })


@app.post('/bookings')
def create_booking():
    data = request.get_json(force=True)
    required = {'council_id', 'hotel', 'cost'}
    if not data or not required.issubset(data):
        abort(400, 'council_id, hotel and cost required')
    council = COUNCILS.get(data['council_id'])
    if not council:
        abort(404, 'council not found')
    cost = float(data['cost'])
    if council.budget_remaining < cost:
        abort(400, 'insufficient funds')
    council.budget_remaining -= cost
    bid = str(uuid.uuid4())
    booking = Booking(id=bid, council_id=council.id, hotel=data['hotel'], cost=cost)
    BOOKINGS[bid] = booking
    council.bookings.append(booking)
    return jsonify({'id': bid, 'hotel': booking.hotel, 'cost': booking.cost}), 201

if __name__ == '__main__':
    app.run(debug=True)
