from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, Boolean, SmallInteger
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class BookAuthor(Base):
    __tablename__ = 'books_authors'
    book_id = Column(SmallInteger, ForeignKey("books.id"))
    author_id = Column(SmallInteger, ForeignKey("authors.id"))


class Book(Base):
    __tablename__ = 'books'

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    title = Column(String(250), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    category_id = Column(SmallInteger, ForeignKey('categories.id'))
    publisher_id = Column(SmallInteger, ForeignKey('publishers.id'))
    category = relationship("Category", back_populates="books")
    publisher = relationship("Publisher", back_populates="books")
    authors = relationship("Author", secondary=BookAuthor.__tablename__, back_populates="books")
    stock = Column(Integer, default=0)
    published_date = Column(DateTime)
    isbn = Column(String(13), unique=True)
    reviews = relationship("Review", back_populates="book")
    order_details = relationship("OrderDetail", back_populates="book")


class Author(Base):
    __tablename__ = 'authors'

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    biography = Column(Text)
    birth_date = Column(DateTime)
    books = relationship("Book", secondary=BookAuthor.__tablename__, back_populates="authors")


class Category(Base):
    __tablename__ = 'categories'

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    books = relationship("Book", back_populates="category")


class Publisher(Base):
    __tablename__ = 'publishers'

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    address = Column(Text)
    books = relationship("Book", back_populates="publisher")


class User(Base):
    __tablename__ = 'users'

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(150), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    orders = relationship("Order", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    addresses = relationship("Address", back_populates="user")


class Order(Base):
    __tablename__ = 'orders'

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    user_id = Column(SmallInteger, ForeignKey('users.id'))
    total_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), nullable=False)
    user = relationship("User", back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order")
    shipping_address_id = Column(SmallInteger, ForeignKey('addresses.id'))
    billing_address_id = Column(SmallInteger, ForeignKey('addresses.id'))
    shipping_address = relationship("Address", foreign_keys=[shipping_address_id])
    billing_address = relationship("Address", foreign_keys=[billing_address_id])


class OrderDetail(Base):
    __tablename__ = 'order_details'

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    order_id = Column(SmallInteger, ForeignKey('orders.id'))
    book_id = Column(SmallInteger, ForeignKey('books.id'))
    quantity = Column(SmallInteger, nullable=False)
    unit_price = Column(Float, nullable=False)
    order = relationship("Order", back_populates="order_details")
    book = relationship("Book", back_populates="order_details")


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    user_id = Column(SmallInteger, ForeignKey('users.id'))
    book_id = Column(SmallInteger, ForeignKey('books.id'))
    rating = Column(SmallInteger, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="reviews")
    book = relationship("Book", back_populates="reviews")


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    user_id = Column(SmallInteger, ForeignKey('users.id'))
    street = Column(String(150), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100))
    country = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    user = relationship("User", back_populates="addresses")
