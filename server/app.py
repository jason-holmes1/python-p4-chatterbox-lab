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
        messages_dict = [msg.to_dict() for msg in messages]
        return make_response(jsonify(messages_dict), 200)

    elif request.method == 'POST':
        new_msg_dict = request.get_json()
        new_message = Message(
            body=new_msg_dict['body'],
            username=new_msg_dict['username']
        )
        db.session.add(new_message)
        db.session.commit()
        return make_response(jsonify(new_message.to_dict()), 201)


@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()
    
    if request.method == 'PATCH':
        updates = request.get_json()
        for field_name, value in updates.items():
            setattr(message, field_name, value)
        db.session.add(message)
        db.session.commit()
        return make_response(jsonify(message.to_dict()), 200)
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return make_response(jsonify({'status': 'delete success'}), 200)


if __name__ == '__main__':
    app.run(port=5555)
