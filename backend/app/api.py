import requests
from flask import Blueprint, request, jsonify
from app import db
import pandas as pd
import json
from app.model import User, Message


api_bp = Blueprint('api', __name__)

@api_bp.route('/test', methods=['POST', 'GET'])
def test():
    model_id = "sentence-transformers/all-MiniLM-L6-v2"
    hf_token = "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"
    api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
    headers = {"Authorization": f"Bearer {hf_token}"}

    def embedding_query(texts):
        response = requests.post(api_url, headers=headers, json={"inputs": texts, "options":{"wait_for_model":True}})
        return response.json()

    texts = ["How do I get a replacement Medicare card?",
            "What is the monthly premium for Medicare Part B?",
            "How do I terminate my Medicare Part B (medical insurance)?",
            "How do I sign up for Medicare?",
            "Can I sign up for Medicare Part B if I am working and have health insurance through an employer?",
            "How do I sign up for Medicare Part B if I already have Part A?",
            "What are Medicare late enrollment penalties?",
            "What is Medicare and who can get it?",
            "How can I get help with my Medicare Part A and Part B premiums?",
            "What are the different parts of Medicare?",
            "Will my Medicare premiums be higher because of my higher income?",
            "What is TRICARE ?",
            "Should I sign up for Medicare Part B if I have Veterans' Benefits?"]

    embeddings = embedding_query(texts)

    output = pd.DataFrame({
        "Text": texts,
        "Embedding": embeddings
    })
    return embeddings

@api_bp.route('/user_message', methods=['GET'])
def receive_user_message():
    data = request.get_json()
    if data:
        return "message recieve"
    else:
        return "fail to recieve"



@api_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = User(name=data['name'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id, 'name': user.name}), 201

@api_bp.route('/messages', methods=['POST'])
def send_message():
    data = request.json
    msg = Message(sender=data['sender'], recipient=data['recipient'], content=data['content'])
    db.session.add(msg)
    db.session.commit()
    return jsonify({'id': msg.id, 'timestamp': msg.timestamp.isoformat()}), 201

@api_bp.route('/messages/<int:user_id>', methods=['GET'])
def get_messages(user_id):
    messages = Message.query.filter((Message.sender == user_id) | (Message.recipient == user_id)).all()
    return jsonify([{
        'id': m.id,
        'from': m.sender,
        'to': m.recipient,
        'content': m.content,
        'timestamp': m.timestamp.isoformat()
    } for m in messages])





@api_bp.route('/test_users/<name>', methods=['GET'])
def create_user_test(name):
    user = User(name=name)
    db.session.add(user)
    db.session.commit()
    return jsonify(message=f'User {name} added successfully!')

@api_bp.route('/get_users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify({user.id: {"name": user.name, "id": user.id} for user in users})



'''
@api_bp.route('/add_user/<name>/<email>', methods=['GET'])
def add_user(name, email):
    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message=f'User {name} added successfully!')

@api_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify({user.id: {"name": user.name, "email": user.email} for user in users})'
'''