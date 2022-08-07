from email.policy import default
from src import Base, Column, String, Integer, ForeignKey, Date, func, Boolean, relationship, engine, UUID, TEXT
import uuid


class Users(Base):  # Users is defined in Base
    __tablename__ = "users_books_store"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(TEXT, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    is_staff = Column(Boolean, nullable=False, default=False)
    create_at = Column(Date, server_default=func.now())
    update_at = Column(Date, default=func.now())

    def __repr__(self):  # __repr__ is defined in Base
        return f"name = {self.name}, usermame = {self.username}"


class Book(Base):  # Book is defined in Base
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    author = Column(Integer, ForeignKey("author.id"), nullable=False)
    year_release = Column(Date)
    year_create = Column(Date)
    genre = Column(String(255))
    price = Column(Integer)
    create_at = Column(Date, server_default=func.now())
    update_at = Column(Date, default=func.now())

    authors = relationship("Author", back_populates="book_author")
    orders = relationship("Order", back_populates="book")

    def __repr__(self):  # __repr__ is defined in Base
        return super().__repr__()


class Author(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    date_of_birth = Column(Date)
    craete_at = Column(Date, server_default=func.now())
    update_at = Column(Date, default=func.now())

    book_author = relationship("Book", back_populates="authors")

    def __repr__(self):  # __repr__ is defined in Base
        return super().__repr__()


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    qty = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)
    order_at = Column(Date, default=func.now())

    book = relationship("Book", back_populates="orders")
    order_rel = relationship("Transaction", back_populates="orders")

    def __repr__(self):  # __repr__ is defined in Base
        return super().__repr__()


class Member(Base):
    __tablename__ = "members"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    craete_at = Column(Date, server_default=func.now())
    update_at = Column(Date, default=func.now())

    def __repr__(self):  # __repr__ is defined in Base
        return super().__repr__()


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    member_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=True)
    total = Column(Integer, nullable=False, default=0)
    qty_items = Column(Integer, nullable=False, default=0)
    create_at = Column(Date, server_default=func.now())

    orders = relationship("Order", back_populates="order_rel")

    def __repr__(self):  # __repr__ is defined in Base
        return super().__repr__()
