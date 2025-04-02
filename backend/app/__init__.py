from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  # Import text from SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/mydatabase'
db = SQLAlchemy(app)


with app.app_context():
    db.create_all()


from app import views #Have to be at the end
from app.api import api_bp
app.register_blueprint(api_bp, url_prefix='/api')
