from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# LoanStatus model
class LoanStatus(Base):
    __tablename__ = 'loan_statuses'
    id = Column(Integer, primary_key=True)
    status = Column(String, nullable=False)


    # LoanGrade model
class LoanGrade(Base):
    __tablename__ = 'loan_grades'
    id = Column(Integer, primary_key=True)
    loan_grades = Column(String, nullable=False)

    # HomeOwnershipType model
class HomeOwnershipType(Base):
    __tablename__ = 'home_ownership_types'
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)

    # LoanIntent model
class LoanIntent(Base):
    __tablename__ = 'loan_intents'
    id = Column(Integer, primary_key=True)
    intent = Column(String, nullable=False)

# Loan model
class Loan(Base):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True)
    person_age = Column(Integer, nullable=False)
    person_home_ownership_type_id = Column(Integer, ForeignKey('home_ownership_types.id'), nullable=False)
    person_emp_length = Column(Float, nullable=False)
    loan_intent_id = Column(Integer, ForeignKey('loan_intents.id'), nullable=False)
    loan_grade_id = Column(Integer, ForeignKey('loan_grades.id'), nullable=False)
    loan_amnt = Column(Float, nullable=False)
    loan_int_rate = Column(Float, nullable=False)
    loan_status_id = Column(Integer, ForeignKey('loan_statuses.id'), nullable=False)
    loan_percent_income = Column(Float, nullable=False)
    cb_person_default_on_file = Column(Integer, nullable=False)
    cb_person_credit_hist_length = Column(Float, nullable=False)

    # Define relationship to loan 
    loan_status = relationship("LoanStatus")
    loan_grade = relationship("LoanGrade")
    home_ownership_type = relationship("HomeOwnershipType")
    loan_intent = relationship("LoanIntent")

