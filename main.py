from fastapi import FastAPI
from telco.main import router as telco_router  # Importamos el router desde telco/main.py

app = FastAPI(title="Mi Proyecto Telco")

# Incluimos el router con prefijo '/telco' (podés cambiar o quitar el prefijo)
app.include_router(telco_router, prefix="/telco")

@app.get("/")
async def root():
    return {"message": "API funcionando correctamente"}
