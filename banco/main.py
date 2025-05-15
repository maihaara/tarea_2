from fastapi import FastAPI, HTTPException
from database.database import SessionLocal, engine
from database import models
import requests
from datetime import datetime

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="API Banco")

TELCO_URL = "http://localhost:8001" 

@app.get("/consultar_deuda/{ci}")
def consultar_deuda(ci: str):
    response = requests.get(f"{TELCO_URL}/consultar_deuda/{ci}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json().get("detail"))
    return response.json()

@app.post("/pagar_deuda/")
def pagar_deuda(nro_factura: str, monto: float, nro_cuenta: str):
    db = SessionLocal()

    cuenta = db.query(models.CuentaDebito).filter(models.CuentaDebito.nro_cuenta == nro_cuenta).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    if cuenta.saldo < monto:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")

    # Consultar deuda actual desde Telco
    factura_res = requests.get(f"{TELCO_URL}/consultar_deuda/{cuenta.cliente.ci}")
    if factura_res.status_code != 200:
        raise HTTPException(status_code=404, detail="No se pudo obtener factura")
    facturas = factura_res.json()
    factura = next((f for f in facturas if f["nrofactura"] == nro_factura), None)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    if monto > factura["saldoPendiente"]:
        raise HTTPException(status_code=400, detail="Monto mayor al saldo pendiente")

    telco_res = requests.post(f"{TELCO_URL}/pagar_deuda/", params={"nro_factura": nro_factura, "monto": monto})
    if telco_res.status_code != 200:
        raise HTTPException(status_code=telco_res.status_code, detail=telco_res.json().get("detail"))

    cuenta.saldo -= monto
    pago = models.PagoServicio(
        fecha=datetime.now().isoformat(),
        id_cuenta_debito=cuenta.id,
        monto=monto,
        nro_factura=nro_factura
    )
    db.add(pago)
    db.commit()
    return {"message": "Pago realizado correctamente"}
