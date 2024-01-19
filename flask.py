from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import Base, User, Blog, Payment  # Import your SQLAlchemy setup

app = Flask(__name__)

# Configure Flask to connect to your database
engine = create_engine('sqlite:///data.db', echo=True)
Base.metadata.bind = engine

# Isolate the creation of the session to avoid global variables
def create_session():
    DBSession = sessionmaker(bind=engine)
    return DBSession()

@app.route('/')
def index():
    session = create_session()
    users = session.query(User).all()
    return render_template('index.html', users=users)

@app.route('/blogs')
def blogs():
    session = create_session()
    blogs = session.query(Blog).all()
    return render_template('blogs.html', blogs=blogs)

@app.route('/payments')
def payments():
    session = create_session()
    payments = session.query(Payment).all()
    return render_template('payments.html', payments=payments)

if __name__ == '__main__':
    app.run(debug=True)

