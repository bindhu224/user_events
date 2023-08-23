from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from sqlalchemy import or_, and_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, jsonify
from flask_restful import Api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'testing secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/userevents'

db = SQLAlchemy(app)
jwt = JWTManager(app)

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=True, help="Title cannot be blank")
parser.add_argument('description', type=str, required=True, help="Description cannot be blank")


@app.route('/event', methods=['POST'])
@jwt_required()
def add_user_event():
    data = parser.parse_args()
    print(f"get_jwt_identity(): {get_jwt_identity()}")
    current_user = User.query.filter_by(id=get_jwt_identity()).first()
    print(f"Current User: {current_user}")
    print(f"Data is: {data}")
    new_event = Event(title=data['title'], description=data['description'], user_id=current_user.id)
    db.session.add(new_event)
    db.session.commit()
    return {'message': 'Event created',
            'event_id':new_event.id,
            'title': new_event.title,
            'description':new_event.description,
            'user_id': new_event.user_id}, 201


class UserEvent(Resource):
    @jwt_required()
    def put(self, event_id):
        data = parser.parse_args()
        event = Event.query.get(event_id)
        if not event:
            return {'message': 'Event not found'}, 404
        event.title = data['title']
        event.description = data['description']
        db.session.commit()
        return {'message': 'Event updated', 'event_id':event.id, 'title': event.title,
                'description':event.description, 'user_id': event.user_id}

    @jwt_required()
    def delete(self, event_id):
        event = Event.query.get(event_id)
        if not event:
            return {'message': 'Event not found'}, 404
        db.session.delete(event)
        db.session.commit()
        return {'message': 'Event deleted'}


@app.route('/user/events', methods=['GET'])
@jwt_required()
def get_user_events():
    current_user = User.query.filter_by(id=get_jwt_identity()).first()
    events = Event.query.filter_by(user_id=current_user.id).all()
    event_list = [{'event_id':event.id,'title': event.title, 'description':event.description,
                   'user_id': event.user_id} for event in events]
    return event_list


@app.route('/events', methods=['GET'])
@jwt_required()
def get_all_events():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    print(title, description)
    if title and description is None:
        events = Event.query.filter_by(title=title).all()
    elif title is None and description:
        events = Event.query.filter_by(description=description).all()
    elif title and description:
        events = Event.query.filter(and_(Event.title==title, Event.description==description)).all()
    elif title is None and description is None:
        events = Event.query.all()

    if not events:
        return {'message': 'Events not found'}, 404
    event_list = [{'event_id':event.id,'title': event.title, 'description': event.description,
                   'user_id': event.user_id} for event in
                  events]
    return event_list


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


@app.cli.command("initdb")
def initdb_command():
    db.create_all()
    print("Database initialized")


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token})
    return jsonify({'message': 'Invalid Credentials'}), 401


api = Api(app)
api.add_resource(UserEvent, '/event/<int:event_id>')

if __name__ == '__main__':
    app.run(port=8080, debug=True)
