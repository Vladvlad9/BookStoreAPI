from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, Boolean, \
    CheckConstraint, Enum, SMALLINT
from sqlalchemy.orm import DeclarativeBase, relationship

from src.enum import UserRole, OrderStatus as order_status

__all__ = [
    "BookAuthor",
    "Book",
    "Author",
    "Category",
    "Publisher",
    "User",
    "OrderStatus",
    "Order",
    "OrderDetail",
    "Review",
    "Address",
    "Discount",
    "BookDiscount",
]


class Base(DeclarativeBase):
    pass


class BookAuthor(Base):
    __tablename__ = 'books_authors'

    id = Column(SMALLINT, primary_key=True)

    book_id = Column(SMALLINT, ForeignKey("books.id"))
    author_id = Column(SMALLINT, ForeignKey("authors.id"))


class BookDiscount(Base):
    __tablename__ = 'book_discounts'

    id = Column(SMALLINT, primary_key=True)

    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    discount_id = Column(Integer, ForeignKey('discounts.id'), nullable=False)


class Book(Base):
    __tablename__ = 'books'

    id = Column(SMALLINT, primary_key=True)

    title = Column(String(250), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    published_date = Column(DateTime)
    isbn = Column(String(13), unique=True)

    category_id = Column(SMALLINT, ForeignKey('categories.id'))
    publisher_id = Column(SMALLINT, ForeignKey('publishers.id'))

    category = relationship("Category", back_populates="books")
    publisher = relationship("Publisher", back_populates="books")
    reviews = relationship("Review", back_populates="book")
    order_details = relationship("OrderDetail", back_populates="book")

    authors = relationship("Author", secondary=BookAuthor.__tablename__, back_populates="books")
    discounts = relationship("Discount", secondary=BookDiscount.__tablename__, back_populates="books")

    __table_args__ = (
        CheckConstraint(price >= 0, name='check_price_positive'),
        CheckConstraint(stock >= 0, name='check_stock_non_negative'),
    )


class Author(Base):
    __tablename__ = 'authors'

    id = Column(SMALLINT, primary_key=True)

    name = Column(String(100), nullable=False)
    biography = Column(Text)
    birth_date = Column(DateTime)

    books = relationship("Book", secondary=BookAuthor.__tablename__, back_populates="authors")


class Category(Base):
    __tablename__ = 'categories'

    id = Column(SMALLINT, primary_key=True)

    name = Column(String(100), nullable=False)
    description = Column(Text)

    books = relationship("Book", back_populates="category")


class Publisher(Base):
    __tablename__ = 'publishers'

    id = Column(SMALLINT, primary_key=True)

    name = Column(String(100), nullable=False)
    address = Column(Text)

    books = relationship("Book", back_populates="publisher")


class User(Base):
    __tablename__ = 'users'

    id = Column(SMALLINT, primary_key=True)

    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(150), nullable=False)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    role = Column(Enum(UserRole), default=UserRole.USER)

    orders = relationship("Order", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    addresses = relationship("Address", back_populates="user")
    roles = relationship("Role", secondary='user_roles')


class OrderStatus(Base):
    __tablename__ = 'order_statuses'

    id = Column(SMALLINT, primary_key=True)

    status = Column(Enum(order_status), nullable=False, unique=True)
    description = Column(Text)

    orders = relationship("Order", back_populates="order_status")


class Order(Base):
    __tablename__ = 'orders'

    id = Column(SMALLINT, primary_key=True)

    user_id = Column(SMALLINT, ForeignKey('users.id'))
    total_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    status_id = Column(SMALLINT, ForeignKey('order_statuses.id'))
    user = relationship("User", back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order")
    shipping_address_id = Column(SMALLINT, ForeignKey('addresses.id'))
    billing_address_id = Column(SMALLINT, ForeignKey('addresses.id'))
    shipping_address = relationship("Address", foreign_keys=[shipping_address_id])
    billing_address = relationship("Address", foreign_keys=[billing_address_id])
    order_status = relationship("OrderStatus", back_populates="orders")


class OrderDetail(Base):
    __tablename__ = 'order_details'

    id = Column(SMALLINT, primary_key=True)

    order_id = Column(SMALLINT, ForeignKey('orders.id'))
    book_id = Column(SMALLINT, ForeignKey('books.id'))
    quantity = Column(SMALLINT, nullable=False)
    unit_price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="order_details")
    book = relationship("Book", back_populates="order_details")


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(SMALLINT, primary_key=True)

    user_id = Column(SMALLINT, ForeignKey('users.id'))
    book_id = Column(SMALLINT, ForeignKey('books.id'))
    rating = Column(SMALLINT, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="reviews")
    book = relationship("Book", back_populates="reviews")

    __table_args__ = (
        CheckConstraint("rating BETWEEN  1 AND  3", name='check_rating_range'),
    )


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(SMALLINT, primary_key=True)

    user_id = Column(SMALLINT, ForeignKey('users.id'))
    street = Column(String(150), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100))
    country = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)

    user = relationship("User", back_populates="addresses")


class Discount(Base):
    __tablename__ = 'discounts'

    id = Column(SMALLINT, primary_key=True)
    code = Column(String(50), unique=True, nullable=False)
    description = Column(Text)

    discount_percent = Column(Float, nullable=False)
    valid_from = Column(DateTime, nullable=False)
    valid_to = Column(DateTime, nullable=False)
    active = Column(Boolean, default=True)

    books = relationship("Book", secondary=BookDiscount.__tablename__, back_populates="discounts")

    __table_args__ = (
        CheckConstraint("discount_percent BETWEEN  1 AND  3", name='check_discount_percent_range'),
    )



