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

# Nuevo reto: crear nuevo reto de endpoint que recia una variable en formato get 
# y que automaticamente, pueda habilitar el formato de hora, 
# como devolver la hora en un formato de 24 hrs

