from database.database import SessionLocal, engine
from database import models
from datetime import datetime

models.Base.metadata.create_all(bind=engine)

def datos():
    db = SessionLocal()

    cliente1 = models.Cliente(nombre="Juan", apellido="Perez", ci="12345678")
    cliente2 = models.Cliente(nombre="Maria", apellido="Gomez", ci="87654321")

    db.add_all([cliente1, cliente2])
    db.commit()

    cuenta1 = models.CuentaDebito(cliente_id=cliente1.id, nro_cuenta="001-123456", saldo=1500.0)
    cuenta2 = models.CuentaDebito(cliente_id=cliente2.id, nro_cuenta="002-654321", saldo=300.0)

    db.add_all([cuenta1, cuenta2])
    db.commit()

    factura1 = models.FacturaPendiente(cliente_id=cliente1.id, nrofactura="F0001", saldoPendiente=500.0)
    factura2 = models.FacturaPendiente(cliente_id=cliente1.id, nrofactura="F0002", saldoPendiente=200.0)
    factura3 = models.FacturaPendiente(cliente_id=cliente2.id, nrofactura="F0003", saldoPendiente=100.0)

    db.add_all([factura1, factura2, factura3])
    db.commit()

    pago1 = models.PagosServicio(fecha=datetime.utcnow().isoformat(), id_cuenta_debito=cuenta1.id, monto=100.0, nro_factura="F0001")
    db.add(pago1)
    db.commit()

    print("Datos de prueba insertados correctamente.")
    db.close()

if __name__ == "__main__":
   datos()
