from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    ci = Column(String, unique=True, index=True, nullable=False)

    cuentas = relationship("CuentaDebito", back_populates="cliente")
    facturas = relationship("FacturaPendiente", back_populates="cliente")

class CuentaDebito(Base):
    __tablename__ = "cuentadebito"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    nro_cuenta = Column(String, unique=True, index=True, nullable=False)
    saldo = Column(Float, default=0.0)

    cliente = relationship("Cliente", back_populates="cuentas")
    pagos = relationship("PagosServicio", back_populates="cuenta")

class FacturaPendiente(Base):
    __tablename__ = "facturapendientes"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    nrofactura = Column(String, unique=True, index=True, nullable=False)
    saldoPendiente = Column(Float, default=0.0)

    cliente = relationship("Cliente", back_populates="facturas")

class PagosServicio(Base):
    __tablename__ = "pagosservicios"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(String, nullable=False)  # ISO 8601
    id_cuenta_debito = Column(Integer, ForeignKey("cuentadebito.id"), nullable=False)
    monto = Column(Float, nullable=False)
    nro_factura = Column(String, nullable=False)

    cuenta = relationship("CuentaDebito", back_populates="pagos")
