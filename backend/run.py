from app import app, db

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)


with app.app_context():
    db.create_all()