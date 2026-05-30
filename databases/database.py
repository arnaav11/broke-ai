# imports
from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Text, Numeric, DateTime
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.exc import IntegrityError
from geoalchemy2 import Geometry

#Create your database
# engine = create_engine("sqlite:///tasks.db", echo=False)
engine = create_engine("sqlite:///data.db", echo=False)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

#Define Models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    plaid_access_token = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    transactions = relationship("Transaction", back_populates="user")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(String, nullable=False)
    transaction = relationship("Transactions", back_populates="category")
    price_indices = relationship("Price Index", back_populates="category")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), index=True, nullable=False)
    amount = Column(Numeric(12,2), nullable=False)
    mechant_name = Column(String, nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)

    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")

class PriceIndex(Base):
    __tablename__ = "prices"

    time = Column(DateTime(timezone=True), primary_key=True, default=lambda: datetime.now(timezone.utc))
    category_id = Column(Integer, ForeignKey("categories.id"), primary_key=True, nullable=False)
    index_value = Column(Numeric(10, 4), nullable=False)
    source = Column(String, nullable=False)

    category = relationship("category", back_populates="prices")

class LocationNode(Base):
    __tablename__ = "location_node"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    merchant_type = Column(String(50), nullable=False)

    location = Column(Geometry('POINT', srid=4326), nullable=False)
