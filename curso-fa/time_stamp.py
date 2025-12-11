from fastapi import FastAPI
from datetime import datetime
import pytz
from pydantic import BaseModel

app = FastAPI()

class TimeResponse(BaseModel):
    timestamp_utc: str
    timestamp_local: str
    timezone: str

@app.get('/hora_actual', response_model=TimeResponse)
def get_current_time():
    """
    Retorna la hora exacta en la que se procesó el request, en UTC y Zona Horaria Local.
    """

    now_utc = datetime.now(pytz.utc)

    mexico_tz = pytz.timezone('America/Mexico_City')
    now_mexico = now_utc.astimezone(mexico_tz)

    return TimeResponse(
        timestamp_utc=now_utc.isoformat(),
        timestamp_local=now_mexico.strftime("%Y-%m-%d %H:%M:%S %Z%z"),
        timezone="America/Mexico_City"
    )

