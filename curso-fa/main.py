import zoneinfo
from datetime import datetime
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hola, Dave!"}

country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}

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
        return { date.isoformat() }
    elif format == 'slash':
        return { date.strftime("%d/%m/%y") }
    elif format == 'written':
        return { date.strftime("%A %d. %B %Y") }
    elif format == 'written':
        return { date.ctime() }
    elif format == 'special':
        return { 'The {1} is {0:%d}, the {2} is {0:%B}.'.format(date, "day", "month") }
    else:
        return {"time without format": datetime.now()}

# Nuevo reto: crear nuevo reto de endpoint que recia una variable en formato get 
# y que automaticamente, pueda habilitar el formato de hora, 
# como devolver la hora en un formato de 24 hrs

