from sqlalchemy import Column, Integer, String, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from database import Base


class FinancialRecord(Base):
    __tablename__ = 'financial_records'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    type_id = Column(Integer, ForeignKey('transaction_types.id', ondelete='CASCADE'), nullable=False)
    subtype_id = Column(Integer, ForeignKey('sub_types.id', ondelete='CASCADE'), nullable=False)
    amount = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    
    user = relationship('Users', back_populates='financial_records')
    transaction_type = relationship('TransactionTypes')
    subtype = relationship('SubTypes')