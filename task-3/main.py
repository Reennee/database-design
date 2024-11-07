from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Loan, LoanIntent, HomeOwnershipType, LoanGrade, LoanStatus
from pydantic import BaseModel
from typing import List
from crud import (
    create_loan_intent, get_loan_intent, get_all_loan_intents,
    update_loan_intent, delete_loan_intent,create_home_ownership_type, get_home_ownership_type, get_all_home_ownership_types, update_home_ownership_type, delete_home_ownership_type,
    create_loan_grade, get_loan_grade, get_all_loan_grades, update_loan_grade, delete_loan_grade,
    create_loan_status, get_loan_status, get_all_loan_statuses, update_loan_status, delete_loan_status
)
from schemas import LoanIntent, LoanIntentCreate, HomeOwnershipType, HomeOwnershipTypeCreate, LoanGrade, LoanGradeCreate, LoanStatus, LoanStatusCreate

DATABASE_URL = "sqlite:///./Dataset/credit.db"

app = FastAPI()

# Set up the database engine and session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize the database
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for the API
class LoanCreate(BaseModel):
    person_age: int
    person_home_ownership_type_id: int
    person_emp_length: float
    loan_intent_id: int
    loan_grade_id: int
    loan_amnt: float
    loan_int_rate: float
    loan_status_id: int
    loan_percent_income: float
    cb_person_default_on_file: int
    cb_person_credit_hist_length: float

# Create loan endpoint
@app.post("/loans/", response_model=LoanCreate, tags=["Loans"])
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    db_loan = Loan(**loan.dict())
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

# Read all loans endpoint
@app.get("/loans/", tags=["Loans"])
def read_loans(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    loans = db.query(Loan).offset(skip).limit(limit).all()
    return loans

# Read loan by ID endpoint
@app.get("/loans/{loan_id}", tags=["Loans"])
def read_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan

# Update loan endpoint
@app.put("/loans/{loan_id}", response_model=LoanCreate, tags=["Loans"])
def update_loan(loan_id: int, loan: LoanCreate, db: Session = Depends(get_db)):
    db_loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    for key, value in loan.dict().items():
        setattr(db_loan, key, value)
    db.commit()
    db.refresh(db_loan)
    return db_loan

# Delete loan endpoint
@app.delete("/loans/{loan_id}", tags=["Loans"])
def delete_loan(loan_id: int, db: Session = Depends(get_db)):
    db_loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    db.delete(db_loan)
    db.commit()
    return {"detail": "Loan deleted successfully"}

# LoanIntent Endpoints
@app.post("/loan_intents/", response_model=LoanIntent, tags=["LoanIntents"])
def create_loan_intent_endpoint(intent: LoanIntentCreate, db: Session = Depends(get_db)):
    return create_loan_intent(db, intent)

@app.get("/loan_intents/{intent_id}", response_model=LoanIntent, tags=["LoanIntents"])
def read_loan_intent(intent_id: int, db: Session = Depends(get_db)):
    loan_intent = get_loan_intent(db, intent_id)
    if loan_intent is None:
        raise HTTPException(status_code=404, detail="Loan Intent not found")
    return loan_intent

@app.get("/loan_intents/", response_model=List[LoanIntent], tags=["LoanIntents"]    )
def read_loan_intents(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_loan_intents(db, skip=skip, limit=limit)

@app.put("/loan_intents/{intent_id}", response_model=LoanIntent, tags=["LoanIntents"])
def update_loan_intent_endpoint(intent_id: int, intent: LoanIntentCreate, db: Session = Depends(get_db)):
    loan_intent = update_loan_intent(db, intent_id, intent)
    if loan_intent is None:
        raise HTTPException(status_code=404, detail="Loan Intent not found")
    return loan_intent

@app.delete("/loan_intents/{intent_id}", tags=["LoanIntents"])
def delete_loan_intent_endpoint(intent_id: int, db: Session = Depends(get_db)):
    loan_intent = delete_loan_intent(db, intent_id)
    if loan_intent is None:
        raise HTTPException(status_code=404, detail="Loan Intent not found")
    return {"detail": "Loan Intent deleted successfully"}


### HomeOwnershipType Endpoints

@app.post("/home_ownership_types/", response_model=HomeOwnershipType, tags=["HomeOwnershipTypes"])
def create_home_ownership_type_endpoint(type: str, db: Session = Depends(get_db)):
    return create_home_ownership_type(db, type)

@app.get("/home_ownership_types/{type_id}", response_model=HomeOwnershipType, tags=["HomeOwnershipTypes"])
def read_home_ownership_type(type_id: int, db: Session = Depends(get_db)):
    home_ownership_type = get_home_ownership_type(db, type_id)
    if home_ownership_type is None:
        raise HTTPException(status_code=404, detail="Home Ownership Type not found")
    return home_ownership_type

@app.get("/home_ownership_types/", response_model=List[HomeOwnershipType], tags=["HomeOwnershipTypes"])
def read_home_ownership_types(db: Session = Depends(get_db)):
    return get_all_home_ownership_types(db)

@app.put("/home_ownership_types/{type_id}", response_model=HomeOwnershipType, tags=["HomeOwnershipTypes"])
def update_home_ownership_type_endpoint(type_id: int, type: str, db: Session = Depends(get_db)):
    home_ownership_type = update_home_ownership_type(db, type_id, type)
    if home_ownership_type is None:
        raise HTTPException(status_code=404, detail="Home Ownership Type not found")
    return home_ownership_type

@app.delete("/home_ownership_types/{type_id}", response_model=HomeOwnershipType, tags=["HomeOwnershipTypes"]    )
def delete_home_ownership_type_endpoint(type_id: int, db: Session = Depends(get_db)):
    home_ownership_type = delete_home_ownership_type(db, type_id)
    if home_ownership_type is None:
        raise HTTPException(status_code=404, detail="Home Ownership Type not found")
    return home_ownership_type

### LoanGrade Endpoints

@app.post("/loan_grades/", response_model=LoanGrade, tags=["LoanGrades"])
def create_loan_grade_endpoint(loan_grades: str, db: Session = Depends(get_db)):
    return create_loan_grade(db, loan_grades)

@app.get("/loan_grades/{grade_id}", response_model=LoanGrade, tags=["LoanGrades"])
def read_loan_grade(grade_id: int, db: Session = Depends(get_db)):
    loan_grade = get_loan_grade(db, grade_id)
    if loan_grade is None:
        raise HTTPException(status_code=404, detail="Loan Grade not found")
    return loan_grade

@app.get("/loan_grades/", response_model=List[LoanGrade], tags=["LoanGrades"])
def read_loan_grades(db: Session = Depends(get_db)):
    return get_all_loan_grades(db)

@app.put("/loan_grades/{grade_id}", response_model=LoanGrade, tags=["LoanGrades"])
def update_loan_grade_endpoint(grade_id: int, loan_grades: str, db: Session = Depends(get_db)):
    loan_grade = update_loan_grade(db, grade_id, loan_grades)
    if loan_grade is None:
        raise HTTPException(status_code=404, detail="Loan Grade not found")
    return loan_grade

@app.delete("/loan_grades/{grade_id}", response_model=LoanGrade, tags=["LoanGrades"])
def delete_loan_grade_endpoint(grade_id: int, db: Session = Depends(get_db)):
    loan_grade = delete_loan_grade(db, grade_id)
    if loan_grade is None:
        raise HTTPException(status_code=404, detail="Loan Grade not found")
    return loan_grade

### LoanStatus Endpoints

@app.post("/loan_statuses/", response_model=LoanStatus, tags=["LoanStatuses"])
def create_loan_status_endpoint(status: str, db: Session = Depends(get_db)):
    return create_loan_status(db, status)

@app.get("/loan_statuses/{status_id}", response_model=LoanStatus, tags=["LoanStatuses"])
def read_loan_status(status_id: int, db: Session = Depends(get_db)):
    loan_status = get_loan_status(db, status_id)
    if loan_status is None:
        raise HTTPException(status_code=404, detail="Loan Status not found")
    return loan_status

@app.get("/loan_statuses/", response_model=List[LoanStatus], tags=["LoanStatuses"])
def read_loan_statuses(db: Session = Depends(get_db)):
    return get_all_loan_statuses(db)

@app.put("/loan_statuses/{status_id}", response_model=LoanStatus, tags=["LoanStatuses"])
def update_loan_status_endpoint(status_id: int, status: str, db: Session = Depends(get_db)):
    loan_status = update_loan_status(db, status_id, status)
    if loan_status is None:
        raise HTTPException(status_code=404, detail="Loan Status not found")
    return loan_status

@app.delete("/loan_statuses/{status_id}", response_model=LoanStatus, tags=["LoanStatuses"])
def delete_loan_status_endpoint(status_id: int, db: Session = Depends(get_db)):
    loan_status = delete_loan_status(db, status_id)
    if loan_status is None:
        raise HTTPException(status_code=404, detail="Loan Status not found")
    return loan_status