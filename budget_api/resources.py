from fastapi import Depends, HTTPException, APIRouter, Query
from typing import List, Optional
from database import get_db
from sqlalchemy.orm import Session
from fastapi_utils.cbv import cbv
from sqlalchemy import and_
from transactions_api import models as tmd
from budget_api import models as md
from budget_api import response_models as rmd

financial_router = APIRouter()

@cbv(financial_router)
class FinancialRecords:
    financial_router.prefix = "/financial"
    financial_router.tags = ["/FinancialRecords"]

    db: Session = Depends(get_db)

    @financial_router.get('/{user_id}', response_model=List[rmd.FinancialRecordResponse])
    def get_records(
        self, 
        user_id: int,
        type_name: Optional[str] = Query(None, description="Filter by type: 'income', 'expenditure', 'savings'"),
        month: Optional[int] = Query(None, ge=1, le=12),
        year: Optional[int] = Query(None)
    ):
        """
        Get all financial records for a user.
        Optional filters: type_name, month, year
        """
        query = self.db.query(md.FinancialRecord).filter(md.FinancialRecord.user_id == user_id)
        print('Type Name***', type_name.lower())
        # Filter by transaction type name if provided
        if type_name:
            type_record = self.db.query(tmd.TransactionTypes)\
                .filter(tmd.TransactionTypes.name == type_name.lower())\
                .first()
            if not type_record:
                raise HTTPException(status_code=400, detail=f"Invalid type: {type_name}")
            query = query.filter(md.FinancialRecord.type_id == type_record.id)
        
        # Apply month/year filters
        if month:
            query = query.filter(md.FinancialRecord.month == month)
        if year:
            query = query.filter(md.FinancialRecord.year == year)
            
        records = query.all()
        return records

    @financial_router.post('/add/{user_id}', response_model=List[rmd.FinancialRecordResponse])
    def add_records(
        self, 
        user_id: int, 
        records: List[rmd.FinancialRecordCreate]
    ):
        """
        Add multiple financial records for a user.
        Each record must specify type_id and subtype_id (not type names).
        """
        new_records = []
        # Validate that all type_id and subtype_id exist
        for record in records:
            # Validate type_id exists
            type_exists = self.db.query(tmd.TransactionTypes)\
                .filter(tmd.TransactionTypes.id == record.type_id)\
                .first()
            if not type_exists:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Transaction type ID {record.type_id} does not exist"
                )
            
            # Validate subtype_id exists and belongs to the type
            subtype_exists = self.db.query(tmd.SubTypes)\
                .filter(
                    and_(
                        tmd.SubTypes.id == record.subtype_id,
                        tmd.SubTypes.type_id == record.type_id
                    )
                ).first()
            if not subtype_exists:
                raise HTTPException(
                    status_code=400,
                    detail=f"Subtype ID {record.subtype_id} does not exist or doesn't belong to type {record.type_id}"
                )
        
        # Create records
        for record in records:
            new_record = md.FinancialRecord(
                user_id=user_id,
                **record.model_dump()
            )
            new_records.append(new_record)
        
        self.db.add_all(new_records)
        self.db.commit()
        
        # Refresh to get IDs and relationships
        for record in new_records:
            self.db.refresh(record)
            
        return new_records

    @financial_router.patch('/edit/{record_id}', response_model=rmd.FinancialRecordResponse)
    def edit_record(
        self, 
        user_id: int, 
        record_id: int, 
        record_update: rmd.FinancialRecordUpdate
    ):
        """
        Edit a specific financial record.
        """
        record = self.db.query(md.FinancialRecord)\
            .filter(
                and_(
                    md.FinancialRecord.user_id == user_id,
                    md.FinancialRecord.id == record_id
                )
            ).first()
            
        if not record:
            raise HTTPException(
                status_code=404, 
                detail=f"Record not found with id: {record_id} for user: {user_id}"
            )
        
        # Validate updated type_id and subtype_id if provided
        update_data = record_update.model_dump(exclude_unset=True)
        
        # Update fields
        for field, value in update_data.items():
            setattr(record, field, value)

        self.db.commit()
        self.db.refresh(record)
        return record

    @financial_router.delete('/delete/{record_id}', response_model=rmd.FinancialRecordResponse)
    def delete_record(self, user_id: int, record_id: int):
        """
        Delete a specific financial record.
        """
        record = self.db.query(md.FinancialRecord)\
            .filter(
                and_(
                    md.FinancialRecord.user_id == user_id,
                    md.FinancialRecord.id == record_id
                )
            ).first()
            
        if not record:
            raise HTTPException(
                status_code=404, 
                detail=f"Record not found with id: {record_id} for user: {user_id}"
            )
            
        self.db.delete(record)
        self.db.commit()
        return record