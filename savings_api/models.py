from sqlalchemy import Column, Integer, String, ForeignKey, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from database import Base

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
