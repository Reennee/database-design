from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Loan(Base):
    __tablename__ = "loans"
    
    id = Column(Integer, primary_key=True, index=True)
    person_age = Column(Integer, nullable=False)
    person_home_ownership_type_id = Column(Integer, ForeignKey("home_ownership_types.id"), nullable=False)
    person_emp_length = Column(Float, nullable=False)
    loan_intent_id = Column(Integer, ForeignKey("loan_intents.id"), nullable=False)
    loan_grade_id = Column(Integer, ForeignKey("loan_grades.id"), nullable=False)
    loan_amnt = Column(Float, nullable=False)
    loan_int_rate = Column(Float, nullable=False)
    loan_status_id = Column(Integer, ForeignKey("loan_statuses.id"), nullable=False)
    loan_percent_income = Column(Float, nullable=False)
    cb_person_default_on_file = Column(Integer, nullable=False)
    cb_person_credit_hist_length = Column(Float, nullable=False)
