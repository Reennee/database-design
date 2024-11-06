from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Loan
from pydantic import BaseModel

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
@app.post("/loans/", response_model=LoanCreate)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    db_loan = Loan(**loan.dict())
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

# Read all loans endpoint
@app.get("/loans/")
def read_loans(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    loans = db.query(Loan).offset(skip).limit(limit).all()
    return loans

# Read loan by ID endpoint
@app.get("/loans/{loan_id}")
def read_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan

# Update loan endpoint
@app.put("/loans/{loan_id}", response_model=LoanCreate)
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
@app.delete("/loans/{loan_id}")
def delete_loan(loan_id: int, db: Session = Depends(get_db)):
    db_loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    db.delete(db_loan)
    db.commit()
    return {"detail": "Loan deleted successfully"}
