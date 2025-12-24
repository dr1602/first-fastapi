# se ejecuta con: fastapi dev app/main.py

from fastapi import HTTPException, status, APIRouter

from models import CustomerCreate, Customer, CustomerUpdate
from db import SessionDep
from sqlmodel import select

router = APIRouter()

db_customers: list[Customer] = []

@router.post('/customers', response_model=Customer, tags=['customers'])
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    # agregamos customers a la sesion
    session.add(customer)
    session.commit() # genera la secuecia de sql y la ejecuta en el motor de la db
    session.refresh(customer) # refrescamos la variable de customer en memoria
    return customer

@router.get('/customers', response_model=list[Customer], tags=['customers'])
async def list_customers(session: SessionDep):
    return session.exec(select(Customer)).all()

@router.get('/customers/{id}', response_model=Customer, tags=['customers'])
async def read_customer(id: int, session: SessionDep):
    customer = session.get(Customer, id)

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No hay cliente con el id {id}'
        )
    
    return customer

@router.delete('/customers/{id}', tags=['customers'])
async def delete_customer(id: int, session: SessionDep):
    customer_db = session.get(Customer, id)

    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No hay cliente con el id {id}'
        )
    
    session.delete(customer_db)
    session.commit()
    return { 'detail': 'ok'}

@router.patch('/customers/{id}', response_model=Customer, status_code=status.HTTP_201_CREATED, tags=['customers'])
async def modify_customer(id: int, customer_data: CustomerUpdate,session: SessionDep):
    customer_db = session.get(Customer, id)

    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No hay cliente con el id {id}'
        )
    
    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer_db.sqlmodel_update(customer_data_dict)

    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)

    return customer_db