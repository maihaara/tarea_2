from fastapi import FastAPI
from telco.main import router as telco_router  

app = FastAPI(title="Mi Proyecto Telco")

app.include_router(telco_router, prefix="/telco")

@app.get("/")
async def root():
    return {"message": "API funcionando correctamente"}
