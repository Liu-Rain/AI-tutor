from app import app, db
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base, sessionmaker


@app.route('/')
def hello():
	return "Hello World!"



