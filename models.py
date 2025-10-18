from sqlalchemy import Column, Integer, String, ForeignKey, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from database import Base


# class Users(Base):
#     __tablename__ = 'users'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='users_pkey'),
#     )

#     id = Column(Integer, primary_key=True)
#     name = Column(String(50), nullable=False)

#     expenditure = relationship('Expenditure', back_populates='users', cascade='all, delete-orphan', passive_deletes=True)
#     income = relationship('Income', back_populates='users', cascade='all, delete-orphan', passive_deletes=True)
#     savings = relationship('Savings', back_populates='users', cascade='all, delete-orphan', passive_deletes=True)


class Expenditure(Base):
    __tablename__ = 'expenditure'
    __table_args__ = (
        ForeignKeyConstraint(
            ['userid'], 
            ['users.id'], 
            name='expenditure_userid_fkey',
            ondelete='CASCADE'
        ),
        PrimaryKeyConstraint('id', name='expenditure_pkey'),
    )

    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False)
    userid = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    amount = Column(Integer, nullable=True)
    month = Column(String(20), nullable=True)
    year = Column(Integer, nullable=True)

    users = relationship('Users', back_populates='expenditure')


class Income(Base):
    __tablename__ = 'income'
    __table_args__ = (
        ForeignKeyConstraint(
            ['userid'], 
            ['users.id'], 
            name='income_userid_fkey', 
            ondelete='CASCADE'
        ),
        PrimaryKeyConstraint('id', name='income_pkey'),
    )

    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False)
    userid = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    amount = Column(Integer, nullable=True)
    month = Column(String(20), nullable=True)
    year = Column(Integer, nullable=True)

    users = relationship('Users', back_populates='income')


class Savings(Base):
    __tablename__ = 'savings'
    __table_args__ = (
        ForeignKeyConstraint(
            ['userid'], 
            ['users.id'], 
            name='savings_userid_fkey',
            ondelete='CASCADE'
        ),
        PrimaryKeyConstraint('id', name='savings_pkey'),
    )

    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False)
    userid = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    amount = Column(Integer, nullable=True)
    month = Column(String(20), nullable=True)
    year = Column(Integer, nullable=True)

    users = relationship('Users', back_populates='savings')


class Transactions(Base):
    __tablename__ = 'transactions'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='transactions_pkey'),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    trans_type = Column(String(20), nullable=False)
    ref_id = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    month = Column(String(20), nullable=False)
    year = Column(Integer, nullable=False)
