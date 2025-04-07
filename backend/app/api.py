import requests
from flask import Blueprint, request, jsonify
from app import db
import pandas as pd
import json
from app.model import User, Message, Conversation
from sqlalchemy.orm import joinedload
from sqlalchemy import or_


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

#This is for frontend test if it has connected succesfully.
@api_bp.route('/user_message', methods=['GET'])
def receive_user_message():
    data = request.get_json()
    if data:
        return "message recieve"
    else:
        return "fail to recieve"

#It will initialize a new conversation for chating and return the conversation's id and title,
@api_bp.route('/conversation_init', methods=['POST'])
def conversation_init():
    data = request.json
    chapter = data['chapter']
    conversation = Conversation(chapter=chapter, title="New Conversation")
    db.session.add(conversation)
    db.session.commit()
    return jsonify({"id":conversation.id, "title":conversation.title})

#it will return all conversation history
@api_bp.route('/fetch_history', methods=['POST'])
def fetch_history():
    data = request.json
    user_id = data['name']
    conversations = db.session.query(Conversation).\
        join(Message).\
        filter(or_(
            Message.sender == user_id,
            Message.recipient == user_id
        )).\
        options(joinedload(Conversation.messages)).\
        distinct().\
        all()
    return conversations

#This will take user input and return LLM response
@api_bp.route('/input', methods=['POST'])
def user_input():
    data = request.json
    conversation_id = data['conversation_id']
    content = data['content']
    conversation_history = []

    conver = Conversation.query.get(conversation_id)
    for mes in conver.messages:
        conversation_history.append({"role": mes.role, "content": mes.content})

    conversation_history.append({"role": "user", "content": content})

    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer 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",
    },

    data=json.dumps({
        "model": "google/gemini-2.5-pro-exp-03-25:free", # Optional
        "messages": conversation_history
    })
    )

    msg = Message(sender=1, recipient=2, role="user", content=content, conversation_id=conversation_id)
    db.session.add(msg)
    db.session.commit()

    text = response.json()
    ai_response = text['choices'][0]['message']['content']

    msg = Message(sender=2, recipient=1, role="assistant", content=ai_response, conversation_id=conversation_id)
    db.session.add(msg)
    db.session.commit()

    return f"AI: {ai_response}"


@api_bp.route('/build')
def build_user():
    chapter = Conversation(chapter="chapter1", title="firstchat")
    db.session.add(chapter)
    db.session.commit()

    user = User(id="Rain")
    db.session.add(user)
    db.session.commit()
    user = User(id="LLM")
    db.session.add(user)
    db.session.commit()
    message = Message(sender="Rain", recipient="LLM", role="system", content="You are a knowledgeable assistant.", conversation_id=1)
    db.session.add(message)
    db.session.commit()
    message = Message(sender="Rain", recipient="LLM", role="user", content="Context: 'We are in Taiwan'", conversation_id=1)
    db.session.add(message)
    db.session.commit()
    return "ok"

@api_bp.route('/test_openrouter')
def test_openrouter():


    #conversation_history = [
    #            {"role": "system", "content": "You are a knowledgeable assistant."},
    #            {"role": "user", "content": f"Context: 'We are in Taiwan'"},
    #        ]
    conversation_history = []
    user_input = "What is love?"

    conver = Conversation.query.get(1)
    for mes in conver.messages:
        conversation_history.append({"role": mes.role, "content": mes.content})

    conversation_history.append({"role": "user", "content": user_input})

    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer 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",
    },

    data=json.dumps({
        "model": "google/gemini-2.5-pro-exp-03-25:free", # Optional
        "messages": conversation_history
    })
    )

    msg = Message(sender="Rain", recipient="LLM", role="user", content=user_input, conversation_id=1)
    db.session.add(msg)
    db.session.commit()
    text = response.json()

    ai_response = text['choices'][0]['message']['content']

    msg = Message(sender="LLM", recipient="Rain", role="assistant", content=ai_response, conversation_id=1)
    db.session.add(msg)
    db.session.commit()
    conversation_history.append({"role": "assistant", "content": ai_response})
    return f"AI: {ai_response},,,,,,,,,,{conversation_history[0]}, {conversation_history[1]}"

@api_bp.route('/messagefromuser')
def messagefromuser():
    user = User.query.get(1)

    # Access all messages the user has sent
    return(f"{user} Sent {user.sent_messages}")


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

@api_bp.route('/get_messages_all', methods=['GET'])
def messs():
    #user = User.query.get(2)
    #return jsonify({mes.id: {"content": mes.content, "id": mes.id, "conversation":mes.conversation_id} for mes in user.sent_messages})
    conver = Conversation.query.get(1)
    return {mes.id: {"content": mes.content, "id": mes.id, "conversation":mes.conversation_id, "sender":mes.sender, "recipient": mes.recipient} for mes in conver.messages}


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