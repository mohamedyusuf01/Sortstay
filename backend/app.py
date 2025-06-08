from datetime import date

from flask import Flask, jsonify, request, abort
from werkzeug.security import generate_password_hash, check_password_hash

from .models import db, init_db, User, Room, Reservation, Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sortstay.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)




@app.post('/register')
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data or 'role' not in data:
        abort(400, 'username, password and role required')
    if User.query.filter_by(username=data['username']).first():
        abort(400, 'user exists')
    user = User(
        username=data['username'],
        password_hash=generate_password_hash(data['password']),
        role=data['role'],
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'status': 'registered'})


@app.post('/login')
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        abort(400, 'username and password required')
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        abort(401)
    token = f"token-{user.id}-{len(Session.query.all())+1}"
    session = Session(token=token, user_id=user.id)
    db.session.add(session)
    db.session.commit()
    return jsonify({'token': token})


def require_auth(role=None):
    """Decorator to enforce token auth and role."""
    def wrapper(f):
        def inner(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                abort(401)
            session_rec = Session.query.filter_by(token=token).first()
            if not session_rec:
                abort(401)
            user = User.query.get(session_rec.user_id)
            if role and user.role != role:
                abort(403)
            request.current_user = user
            return f(*args, **kwargs)
        inner.__name__ = f.__name__
        return inner
    return wrapper

@app.post('/availability')
@require_auth(role='hotel')
def add_availability():
    """Hotels post available rooms here."""
    data = request.get_json()
    if not data or 'room_id' not in data:
        abort(400, 'room_id required')
    room = Room(
        hotel=request.current_user.username,
        room_id=data['room_id'],
        price=data.get('price'),
        date_available=data.get('date_available', date.today()),
    )
    db.session.add(room)
    db.session.commit()
    return jsonify({'status': 'added', 'id': room.id}), 201


@app.get('/rooms')
@require_auth()
def list_rooms():
    """List all currently available rooms."""
    rooms = Room.query.filter_by(is_available=True).all()
    data = [
        {
            'id': r.id,
            'hotel': r.hotel,
            'room_id': r.room_id,
            'price': r.price,
            'date_available': r.date_available.isoformat() if r.date_available else None,
        }
        for r in rooms
    ]
    return jsonify({'rooms': data})


@app.post('/book')
@require_auth(role='council')
def book_room():
    """Councils book a room by room_id."""
    data = request.get_json()
    if not data or 'room_id' not in data:
        abort(400, 'room_id required')
    room = Room.query.filter_by(room_id=data['room_id'], is_available=True).first()
    if not room:
        abort(404, 'room not found')
    nights = data.get('nights', 1)
    room.is_available = False
    reservation = Reservation(
        room_id=room.id,
        user_id=request.current_user.id,
        nights=nights,
        total_cost=room.price * nights if room.price else None,
    )
    db.session.add(reservation)
    db.session.commit()
    return jsonify({'status': 'booked', 'reservation_id': reservation.id})

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)
