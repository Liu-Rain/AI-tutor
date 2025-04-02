from app import app, db
from sqlalchemy import text  # Import text from SQLAlchemy

@app.route('/')
def hello():
	return "Hello World!"



#example function
@app.route('/check_db')
def check_db():
    try:
        db.session.execute(text('SELECT 1'))  # Simple test query
        return "Database is connected!"
    except Exception as e:
        return f"Database connection failed: {str(e)}"

#example function
# Define a model for the table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'
    
#example function
# Create the tables
with app.app_context():
    db.create_all()
    
#example function
# example: add_user/Rain/Rain_email@example.com
@app.route('/add_user/<name>/<email>')
def add_user(name, email):
    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()
    return f'User {name} added successfully!'

#example function
@app.route('/users')
def get_users():
    users = User.query.all()
    return {user.id: {"name": user.name, "email": user.email} for user in users}