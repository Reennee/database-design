from sqlalchemy.orm import Session
from models import Loan
from schemas import LoanCreate

def get_loan(db: Session, loan_id: int):
    return db.query(Loan).filter(Loan.id == loan_id).first()

def get_loans(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Loan).offset(skip).limit(limit).all()

def create_loan(db: Session, loan: LoanCreate):
    db_loan = Loan(**loan.dict())
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

def update_loan(db: Session, loan_id: int, loan_data: dict):
    db_loan = get_loan(db, loan_id)
    if db_loan:
        for key, value in loan_data.items():
            setattr(db_loan, key, value)
        db.commit()
        db.refresh(db_loan)
    return db_loan

def delete_loan(db: Session, loan_id: int):
    db_loan = get_loan(db, loan_id)
    if db_loan:
        db.delete(db_loan)
        db.commit()
    return db_loan
