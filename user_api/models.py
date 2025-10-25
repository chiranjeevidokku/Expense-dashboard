from sqlalchemy import Column, Integer, String, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from database import Base

class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    # Single relationship for all financial records
    financial_records = relationship(
        'FinancialRecord', 
        back_populates='user', 
        cascade='all, delete-orphan', 
        passive_deletes=True
    )