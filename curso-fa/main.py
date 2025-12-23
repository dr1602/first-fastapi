import zoneinfo
from datetime import datetime
from fastapi import FastAPI, HTTPException, status

from models import CustomerCreate, Transaction, Invoice, Customer, CustomerUpdate
from db import SessionDep, create_all_tables
from sqlmodel import select

country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}

app = FastAPI(lifespan=create_all_tables)

@app.get("/")
async def root():
    return {"message": "Hola, Dave!"}

@app.get("/time")
async def specific_time():
    return {"time": datetime.now()}

@app.get("/time/{iso_code}")
async def multiple_times(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time": datetime.now(tz)}

@app.get("/time/format/{format_code}")
async def formatted_time(format_code: str):
    format = format_code.lower()
    date = datetime.now()
    if format == 'iso':
        return { date.isoformat() } # '2002-03-11'
    elif format == 'slash':
        return { date.strftime("%d/%m/%y") } # '11/03/02'
    elif format == 'written':
        return { date.strftime("%A %d. %B %Y") } # 'Monday 11. March 2002'
    elif format == 'spaced':
        return { date.ctime() } # 'Mon Mar 11 00:00:00 2002'
    elif format == 'special':
        return { 'The {1} is {0:%d}, the {2} is {0:%B}.'.format(date, "day", "month") } # 'The day is 11, the month is March.'
    else:
        return {"time without format": datetime.now()}
    
db_customers: list[Customer] = []

@app.post('/customers', response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    # agregamos customers a la sesion
    session.add(customer)
    session.commit() # genera la secuecia de sql y la ejecuta en el motor de la db
    session.refresh(customer) # refrescamos la variable de customer en memoria
    return customer

@app.get('/customers', response_model=list[Customer])
async def list_customers(session: SessionDep):
    return session.exec(select(Customer)).all()

@app.get('/customers/{id}', response_model=Customer)
async def read_customer(id: int, session: SessionDep):
    customer = session.get(Customer, id)

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No hay cliente con el id {id}'
        )
    
    return customer

@app.delete('/customers/{id}')
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

@app.patch('/customers/{id}', response_model=Customer, status_code=status.HTTP_201_CREATED)
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

@app.post('/transactions')
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@app.post('/invoices')
async def create_invoices(invoice_data: Invoice):
    return invoice_data

