from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base

class RegistroContable(Base):
    __tablename__ = "registros_contables"

    # Columnas basadas en la imagen (ajustadas a nombres snake_case)
    id = Column(Integer, primary_key=True, index=True, name="N°")
    usuario = Column(String, index=True)
    n_factura = Column(String)
    fecha_factura = Column(String) # Usar String por la dificultad de parsear Date en SQLite sin librerias extra
    ref_bancaria = Column(String)
    carnet = Column(String)
    nombres = Column(String)
    rubro = Column(String)
    cod_pago = Column(String)
    detalle = Column(String)
    monto_total = Column(Float)
    objeto = Column(String)
    volteos = Column(String)
    monto_siscom = Column(Float)
    monto_extracto = Column(Float)
    diferencia_monto = Column(Float)
    observacion = Column(String)