from sqlalchemy import Column, Integer, String, Float, Date, UniqueConstraint
from .database import Base

class RegistroContable(Base):
    __tablename__ = "registros_contables"

    # 🚨 NOTA IMPORTANTE: Se asume que n_factura y rubro forman la clave única.
    # Se añade UniqueConstraint al final.

    # Columnas basadas en el esquema (ajustadas a nombres snake_case)
    # n_factura y rubro son las claves únicas para evitar duplicados.
    id = Column(Integer, primary_key=True, index=True, name="N°") 
    usuario = Column(String, index=True)
    n_factura = Column(String) # Lo dejo como String por si contiene prefijos/sufijos
    fecha_factura = Column(String) 
    ref_bancaria = Column(String)
    carnet = Column(String)
    nombres = Column(String)
    rubro = Column(String) # Lo dejo como String para alinearlo con el Constraint y el CSV
    cod_pago = Column(String)
    detalle = Column(String)
    monto_total = Column(Float)
    objeto = Column(String)
    volteos = Column(String) # Lo dejo como String ya que tenía texto no numérico en el error
    monto_siscom = Column(Float)
    monto_extracto = Column(Float)
    diferencia_monto = Column(Float)
    observacion = Column(String)

    # 🚨 RESTRICCIÓN DE UNICIDAD COMPUESTA 🚨
    # Esto asegura que no se inserten filas con el mismo número de factura y rubro.
    __table_args__ = (
        UniqueConstraint('n_factura', 'rubro', name='_factura_rubro_uc'),
    )