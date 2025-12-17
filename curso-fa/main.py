import zoneinfo
from datetime import datetime
from fastapi import FastAPI
from models import Customer, Transaction, Invoice

country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}

app = FastAPI()

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

@app.post('/customers')
async def create_customer(customer_data: Customer):
    return customer_data

@app.post('/transactions')
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@app.post('/invoices')
async def create_invoices(invoice_data: Invoice):
    return invoice_data