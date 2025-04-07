from datetime import datetime, timedelta, timezone
from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(100), primary_key=True)

    sent_messages = db.relationship('Message', back_populates='sender_user', foreign_keys='Message.sender')
    received_messages = db.relationship('Message', back_populates='recipient_user', foreign_keys='Message.recipient')

class Conversation(db.Model):
    __tablename__ = 'conversations'
    id = db.Column(db.Integer, primary_key=True)
    chapter = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    # Add relationship to messages
    messages = db.relationship('Message', back_populates='conversation', cascade='all, delete-orphan')


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100), db.ForeignKey('users.id'), nullable=False)
    recipient = db.Column(db.String(100), db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now().astimezone(timezone(timedelta(hours=9, minutes=30))))
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    
    conversation = db.relationship('Conversation', back_populates='messages')
    sender_user = db.relationship('User', back_populates='sent_messages', foreign_keys=[sender])
    recipient_user = db.relationship('User', back_populates='received_messages', foreign_keys=[recipient])

