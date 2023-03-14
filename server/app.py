from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at).all()
        return jsonify([msg.to_dict() for msg in messages]), 200
    elif request.method == 'POST':
        json_msg = request.get_json()
        new_message = Message(
            body=json_msg['body'],
            username=json_msg['username']
        )
        db.session.add(new_message)
        db.session.commit()
        return jsonify(new_message.to_dict()), 201

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()

    if not message:
        return jsonify({'error': 'message not found'}), 404

    if request.method == 'PATCH':
        json_msg = request.get_json()
        for field, value in json_msg.items():
            setattr(message, field, value)
        db.session.add(message)
        db.session.commit()
        return jsonify(message.to_dict()), 200
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return jsonify({'message': 'delete success'})


if __name__ == '__main__':
    app.run(port=5555)
