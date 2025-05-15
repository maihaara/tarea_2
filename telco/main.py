from fastapi import FastAPI, HTTPException, Query
from database.database import SessionLocal, engine
from database import models
from sqlalchemy.orm import Session
from datetime import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Telco API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/consultar_deuda/{ci}")
def consultar_deuda(ci: str):
    db = next(get_db())
    cliente = db.query(models.Cliente).filter(models.Cliente.ci == ci).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    facturas = db.query(models.FacturaPendiente).filter(
        models.FacturaPendiente.cliente_id == cliente.id,
        models.FacturaPendiente.saldoPendiente > 0
    ).all()

    resultado = [
        {
            "nrofactura": f.nrofactura,
            "saldoPendiente": f.saldoPendiente
        } for f in facturas
    ]
    return {"cliente": f"{cliente.nombre} {cliente.apellido}", "facturas_pendientes": resultado}

@app.post("/pagar_deuda")
def pagar_deuda(
    nro_factura: str = Query(...),
    monto: float = Query(...)
):
    db = next(get_db())
    factura = db.query(models.FacturaPendiente).filter(
        models.FacturaPendiente.nrofactura == nro_factura
    ).first()
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    if monto <= 0:
        raise HTTPException(status_code=422, detail="Monto debe ser positivo")

    if monto > factura.saldoPendiente:
        raise HTTPException(status_code=422, detail="Monto supera el saldo pendiente")

    factura.saldoPendiente -= monto
    db.commit()

    return {"mensaje": f"Pago de {monto} aplicado correctamente a la factura {nro_factura}"}
