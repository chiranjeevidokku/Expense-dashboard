from fastapi import Depends, HTTPException, APIRouter, Query
from typing import List, Optional
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi_utils.cbv import cbv
from transactions_api import models as md
from transactions_api import reponse_models as rmd

transaction_api = APIRouter()

@cbv(transaction_api)
class Transactions:
    transaction_api.prefix = "/transactions"
    transaction_api.tags = ["/Transactions"]

    db: Session = Depends(get_db)

    @transaction_api.get('/{user_id}', response_model=List[rmd.TransactionResponsetModel])
    def get_transactions(
        self, 
        user_id: int, 
        type_name: Optional[str] = Query(None, description="Filter by type: 'income', 'expenditure', 'savings'"),
        month: Optional[int] = Query(None, ge=1, le=12),
        year: Optional[int] = Query(None)
        ):
        query = self.db.query(md.Transactions).filter(md.Transactions.user_id == user_id)
        if type_name:
            record = self.db.query(md.TransactionTypes)\
                .filter(md.TransactionTypes.name == type_name.lower())\
                .first()
            if not record:
                raise HTTPException(status_code=404, detail=f"Invalid Type: {type_name}")
            query = query.filter(md.Transactions.transtype_id == record.id)
        if month:
            query = query.filter(md.Transactions.month == month)
        if year:
            query = query.filter(md.Transactions.year == year)
        records = query.all()
        return records
    
    @transaction_api.post('/add/{user_id}', response_model=List[rmd.TransactionResponsetModel])
    def add_transactions(
        self, 
        user_id: int, 
        records: List[rmd.TransactionCreateRecord]
        ):
        new_records = []
        for record in records:
            type_exits = self.db.query(md.TransactionTypes)\
                .filter(md.TransactionTypes.id == record.transtype_id)\
                .first()
            if not type_exits:
                raise HTTPException(status_code=404, detail=f"Invalid Transaction Id: {record.transtype_id}")
            
            subtype_exist = self.db.query(md.SubTypes)\
                .filter(
                    and_(
                        md.SubTypes.id == record.subtype_id,
                        md.SubTypes.type_id == record.transtype_id
                        ))\
                .first()
            if not subtype_exist:
                raise HTTPException(
                    status_code=404, 
                    detail=f"Subtype ID {record.subtype_id} does not exist or doesn't belong to type {record.transtype_id}"
                    )
            
        for record in records:
            new_record = md.Transactions(
                user_id = user_id,
                **record.model_dump()
            )
            new_records.append(new_record)
        self.db.add_all(new_records)
        self.db.commit()

        for record in new_records:
            self.db.refresh(record)
        return new_records
    
    @transaction_api.patch('/edit/{record_id}', response_model=rmd.TransactionResponsetModel)
    def edit_transactions(
        self,
        user_id: int,
        record_id: int,
        record_update: rmd.TransactionUpdateRecord
    ):
        record = self.db.query(md.Transactions)\
            .filter(
                and_(
                    md.Transactions.user_id == user_id,
                    md.Transactions.id == record_id
                )
            )\
            .first()
        if not record:
            raise HTTPException(
                status_code=404, 
                detail=f"Record not found with id: {record_id} for user: {user_id}"
            )
        update_data = record_update.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(record, field, value)

        self.db.commit()
        self.db.refresh(record)
        return record

    @transaction_api.delete('/delete{record_id}', response_model=rmd.TransactionResponsetModel)
    def delete_transaction(
        self,
        record_id: int,
        user_id: int
    ):
        record = self.db.query(md.Transactions)\
            .filter(
                and_(
                    md.Transactions.id == record_id,
                    md.Transactions.user_id == user_id
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



