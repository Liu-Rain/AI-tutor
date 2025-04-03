from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    sent_messages = db.relationship('Message', back_populates='sender_user', foreign_keys='Message.sender')
    received_messages = db.relationship('Message', back_populates='recipient_user', foreign_keys='Message.recipient')

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    sender_user = db.relationship('User', back_populates='sent_messages', foreign_keys=[sender])
    recipient_user = db.relationship('User', back_populates='received_messages', foreign_keys=[recipient])
