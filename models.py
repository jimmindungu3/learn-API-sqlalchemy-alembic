# models.py

from sqlalchemy import create_engine, Column, Integer, String, Sequence, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from faker import Faker

fake = Faker()

engine = create_engine('sqlite:///data.db', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String(50), unique=True)
    full_name = Column(String(50))
    email = Column(String(100))
    blogs = relationship('Blog', back_populates='author')
    payments = relationship('Payment', back_populates='user')

class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, Sequence('blog_id_seq'), primary_key=True)
    title = Column(String(100))
    content = Column(String(500))
    user_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('User', back_populates='blogs')
    payments = relationship('Payment', back_populates='blog')

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, Sequence('payment_id_seq'), primary_key=True)
    amount = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id'))
    blog_id = Column(Integer, ForeignKey('blogs.id'))
    user = relationship('User', back_populates='payments')
    blog = relationship('Blog', back_populates='payments')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

for _ in range(5):
    new_user = User(username=fake.user_name(), email=fake.email(), full_name=fake.name())
    session.add(new_user)

session.commit()

for _ in range(10):
    new_blog = Blog(title=fake.sentence(), content=fake.paragraph(), author=fake.random_element(session.query(User).all()))
    session.add(new_blog)

session.commit()

for _ in range(15):
    amount = fake.random_int(min=10, max=100)
    user = fake.random_element(session.query(User).all())
    blog = fake.random_element(session.query(Blog).all())
    new_payment = Payment(amount=amount, user=user, blog=blog)
    session.add(new_payment)

session.commit()
print("Users, Blogs, and Payments added successfully")

session.close()

