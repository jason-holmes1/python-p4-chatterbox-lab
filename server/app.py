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

@app.get('/messages')
def get_messages():
    msgs = Message.query.order_by(Message.created_at).all()
    body = [m.to_dict() for m in msgs]
    return body, 200

@app.post('/messages')
def post_messages():
    msg_data = request.get_json()
    new_msg = Message(
        body=msg_data.get('body'),
        username=msg_data.get('username')
    )
    db.session.add(new_msg)
    db.session.commit()
    return new_msg.to_dict(), 201

@app.delete('/messages/<int:id>')
def delete_message(id):
    msg = Message.query.filter(Message.id == id).first()

    if msg is None:
        return {'message': 'message not found'}, 404
    
    db.session.delete(msg)
    db.session.commit()

    return {}, 200

@app.patch('/messages/<int:id>')
def patch_message(id):
    msg = Message.query.filter(Message.id == id).first()

    if msg is None:
        return {'message': 'message not found'}, 404
    
    msg_data = request.get_json()

    for field in msg_data:
        setattr(msg, field, msg_data[field])

    db.session.add(msg)
    db.session.commit()

    return msg.to_dict(), 200

@app.route('/messages/<int:id>')
def messages_by_id(id):
    msg = Message.query.filter(Message.id == id).first()

    if msg is None:
        return {'message': 'message not found'}, 404

    return msg.to_dict(), 200

if __name__ == '__main__':
    app.run(port=5555)
