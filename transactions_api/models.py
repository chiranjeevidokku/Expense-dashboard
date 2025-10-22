from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class TransactionTypes(Base):
    __tablename__ = 'transaction_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    subtypes = relationship('SubTypes', back_populates='transaction_type')

class SubTypes(Base):
    __tablename__ = 'sub_types'
    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('transaction_types.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(50), nullable=False)
    transaction_type = relationship('TransactionTypes', back_populates='subtypes')

class Transactions(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    transtype_id = Column(Integer, ForeignKey('transaction_types.id', ondelete='CASCADE'), nullable=False)
    subtype_id = Column(Integer, ForeignKey('sub_types.id', ondelete='CASCADE'), nullable=False)
    amount = Column(Integer, nullable=True)
    month = Column(String(20), nullable=True)
    year = Column(Integer, nullable=True)