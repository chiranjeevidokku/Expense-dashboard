
from sqlalchemy import Column, Integer, String, ForeignKey, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from database import Base

class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    expenditure = relationship('Expenditure', back_populates='users', cascade='all, delete-orphan', passive_deletes=True)
    income = relationship('Income', back_populates='users', cascade='all, delete-orphan', passive_deletes=True)
    savings = relationship('Savings', back_populates='users', cascade='all, delete-orphan', passive_deletes=True)
