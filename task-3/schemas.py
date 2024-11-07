from pydantic import BaseModel

# LoanIntent Pydantic models
class LoanIntentBase(BaseModel):
    intent: str

class LoanIntentCreate(LoanIntentBase):
    pass

class LoanIntent(LoanIntentBase):
    id: int
    class Config:
        orm_mode = True

# HomeOwnershipType Pydantic models
class HomeOwnershipTypeBase(BaseModel):
    type: str

class HomeOwnershipTypeCreate(HomeOwnershipTypeBase):
    pass

class HomeOwnershipType(HomeOwnershipTypeBase):
    id: int
    class Config:
        orm_mode = True

# LoanGrade Pydantic models
class LoanGradeBase(BaseModel):
    loan_grades: str

class LoanGradeCreate(LoanGradeBase):
    pass

class LoanGrade(LoanGradeBase):
    id: int
    class Config:
        orm_mode = True

# LoanStatus Pydantic models
class LoanStatusBase(BaseModel):
    status: str

class LoanStatusCreate(LoanStatusBase):
    pass

class LoanStatus(LoanStatusBase):
    id: int
    class Config:
        orm_mode = True
