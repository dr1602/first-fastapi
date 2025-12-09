from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hola, Dave!"}

# Para correr ejecuta: fastapi dev
# api: http://localhost:8000/
# swagger: http://localhost:8000/docs