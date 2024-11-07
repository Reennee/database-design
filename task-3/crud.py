from sqlalchemy.orm import Session
from models import LoanStatus, Loan, LoanGrade, HomeOwnershipType, LoanIntent

# CRUD operations for LoanStatus
def create_loan_status(db: Session, status: str):
    new_status = LoanStatus(status=status)
    db.add(new_status)
    db.commit()
    db.refresh(new_status)
    return new_status

def get_loan_status(db: Session, status_id: int):
    return db.query(LoanStatus).filter(LoanStatus.id == status_id).first()

def get_all_loan_statuses(db: Session):
    return db.query(LoanStatus).all()

def update_loan_status(db: Session, status_id: int, status: str):
    loan_status = db.query(LoanStatus).filter(LoanStatus.id == status_id).first()
    if loan_status:
        loan_status.status = status
        db.commit()
        db.refresh(loan_status)
    return loan_status

def delete_loan_status(db: Session, status_id: int):
    loan_status = db.query(LoanStatus).filter(LoanStatus.id == status_id).first()
    if loan_status:
        db.delete(loan_status)
        db.commit()
    return loan_status

# CRUD operations for Loan
def create_loan(db: Session, loan_data: dict):
    new_loan = Loan(**loan_data)
    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)
    return new_loan

def get_loan(db: Session, loan_id: int):
    return db.query(Loan).filter(Loan.id == loan_id).first()

def get_all_loans(db: Session):
    return db.query(Loan).all()

def update_loan(db: Session, loan_id: int, loan_data: dict):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if loan:
        for key, value in loan_data.items():
            setattr(loan, key, value)
        db.commit()
        db.refresh(loan)
    return loan

def delete_loan(db: Session, loan_id: int):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if loan:
        db.delete(loan)
        db.commit()
    return loan


# CRUD operations for LoanGrade
def create_loan_grade(db: Session, grade: str):
    new_grade = LoanGrade(loan_grades=grade)
    db.add(new_grade)
    db.commit()
    db.refresh(new_grade)
    return new_grade

def get_loan_grade(db: Session, grade_id: int):
    return db.query(LoanGrade).filter(LoanGrade.id == grade_id).first()

def get_all_loan_grades(db: Session):
    return db.query(LoanGrade).all()

def update_loan_grade(db: Session, grade_id: int, grade: str):
    loan_grade = db.query(LoanGrade).filter(LoanGrade.id == grade_id).first()
    if loan_grade:
        loan_grade.loan_grades = grade
        db.commit()
        db.refresh(loan_grade)
    return loan_grade

def delete_loan_grade(db: Session, grade_id: int):
    loan_grade = db.query(LoanGrade).filter(LoanGrade.id == grade_id).first()
    if loan_grade:
        db.delete(loan_grade)
        db.commit()
    return loan_grade

# CRUD operations for HomeOwnershipType
def create_home_ownership_type(db: Session, ownership_type: str):
    new_home_ownership_type = HomeOwnershipType(type=ownership_type)
    db.add(new_home_ownership_type)
    db.commit()
    db.refresh(new_home_ownership_type)
    return new_home_ownership_type

def get_home_ownership_type(db: Session, type_id: int):
    return db.query(HomeOwnershipType).filter(HomeOwnershipType.id == type_id).first()

def get_all_home_ownership_types(db: Session):
    return db.query(HomeOwnershipType).all()

def update_home_ownership_type(db: Session, type_id: int, ownership_type: str):
    home_ownership_type = db.query(HomeOwnershipType).filter(HomeOwnershipType.id == type_id).first()
    if home_ownership_type:
        home_ownership_type.type = ownership_type
        db.commit()
        db.refresh(home_ownership_type)
    return home_ownership_type

def delete_home_ownership_type(db: Session, type_id: int):
    home_ownership_type = db.query(HomeOwnershipType).filter(HomeOwnershipType.id == type_id).first()
    if home_ownership_type:
        db.delete(home_ownership_type)
        db.commit()
    return home_ownership_type

# CRUD operations for LoanIntent
def create_loan_intent(db: Session, intent: str):
    new_loan_intent = LoanIntent(intent=intent)
    db.add(new_loan_intent)
    db.commit()
    db.refresh(new_loan_intent)
    return new_loan_intent

def get_loan_intent(db: Session, intent_id: int):
    return db.query(LoanIntent).filter(LoanIntent.id == intent_id).first()

def get_all_loan_intents(db: Session):
    return db.query(LoanIntent).all()

def update_loan_intent(db: Session, intent_id: int, intent: str):
    loan_intent = db.query(LoanIntent).filter(LoanIntent.id == intent_id).first()
    if loan_intent:
        loan_intent.intent = intent
        db.commit()
        db.refresh(loan_intent)
    return loan_intent

def delete_loan_intent(db: Session, intent_id: int):
    loan_intent = db.query(LoanIntent).filter(LoanIntent.id == intent_id).first()
    if loan_intent:
        db.delete(loan_intent)
        db.commit()
    return loan_intent