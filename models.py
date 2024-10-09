from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    books = relationship('Book', back_populates='author')


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    books = relationship('Book', back_populates='category')


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))

    author = relationship('Author', back_populates='books')
    category = relationship('Category', back_populates='books')


class PurchaseRequests(Base):
    __tablename__ = "purchase_requests"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id'))  # Correct the table name to 'books'
    reader_name = Column(String)  # Remove ForeignKey for reader_name, use String instead
    payment_details = Column(String)
    status = Column(String, default='pending')  # pending, approved, rejected

    book = relationship('Book')  # This remains the same


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    full_name = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    role = Column(String)
    disabled = Column(Boolean, default=False)
