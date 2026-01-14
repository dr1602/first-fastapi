from typing import Optional
from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field, Relationship

# Creamos una tabla intermedia para conectar los planes con los customers
class CustomerPlan(SQLModel, table=True):
    id: int = Field(primary_key=True)
    plan_id: int = Field(foreign_key='plan.id')
    customer_id: int = Field(foreign_key='customer.id')

# Creamos la base para los planes
class Plan(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    name: str = Field(default=None)
    price: int = Field(default=None)
    description: str = Field(default=None)
    customers: list['Customer'] = Relationship(
        back_populates='plans', link_model=CustomerPlan
    )

# aquí no se crea la tabla porque no hay table true, y es para recibir datos 
class CustomerBase(SQLModel):
    # Field es para definir que se debe de guardar en la base de datos
    name: str = Field(default=None)
    description: str | None = Field(default=None)
    email: EmailStr = Field(default=None)
    age: int = Field(default=None)

# me parece que aqui activas la tabla
class Customer(CustomerBase, table=True):  # donde tiene true porque es donde vamos a crear campos
    # Field es para definir que se debe de guardar en la base de datos
    id: int | None = Field(default=None, primary_key=True)
    ### vincula el customer con el transaction
    transactions: list['Transaction'] = Relationship(back_populates='customer')# no creará nuevos campos, campo de relación, no permitirá obtener datos. guardaremos la lista de todas las transacciones, para mostrarlas en nuestro objeto en memori
    plans: list[Plan] = Relationship(
        back_populates='customers', link_model=CustomerPlan
    )

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int]= None

class CustomerUpdate(CustomerUpdate):
    pass

class TransactionBase(SQLModel):
    amount: int
    description: str

class TransactionRead(TransactionBase):
    id: int

class CustomerRead(CustomerBase):
    id: int

class CustomerReadWithTransactions(CustomerRead):
    transactions: list[TransactionRead] = []

class Transaction(TransactionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key='customer.id')
    ### vincula el customer con el transaction
    customer: Customer = Relationship(back_populates='transactions')

class TransactionCreate(TransactionBase):
    customer_id: int = Field(foreign_key='customer.id')

class Invoice(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: int

    @property
    def amount_total(self):
        return sum(transaction.amount for transaction in self.transactions)
