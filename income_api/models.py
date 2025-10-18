from sqlalchemy import Column, Integer, String, ForeignKey, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from database import Base

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