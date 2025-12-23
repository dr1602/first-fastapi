from typing import Optional
from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field

# aquí no se crea la tabla porque no hay table true, y es para recibir datos 
class CustomerBase(SQLModel):
    # Field es para definir que se debe de guardar en la base de datos
    name: str = Field(default=None)
    description: str | None = Field(default=None)
    email: EmailStr = Field(default=None)
    age: int = Field(default=None)

# me parece que aqui activas la tabla
class Customer(CustomerBase, table=True):
    # Field es para definir que se debe de guardar en la base de datos
    id: int | None = Field(default=None, primary_key=True)

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int]= None

class CustomerUpdate(CustomerUpdate):
    pass

class Transaction(BaseModel):
    id: int
    amount: int
    description: str

class Invoice(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: int

    @property
    def amount_total(self):
        return sum(Transaction.amount for transaction in self.transactions)
