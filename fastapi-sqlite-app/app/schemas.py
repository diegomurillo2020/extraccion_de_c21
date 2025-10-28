from pydantic import BaseModel
from datetime import date

# 🆕 Esquemas para RegistroContable

class RegistroBase(BaseModel):
    usuario: str
    n_factura: str
    fecha_factura: str 
    ref_bancaria: str
    carnet: str
    nombres: str
    rubro: str
    cod_pago: str
    detalle: str | None = None
    monto_total: float
    objeto: str | None = None
    volteos: str | None = None
    monto_siscom: float
    monto_extracto: float
    diferencia_monto: float
    observacion: str | None = None

class RegistroCreate(RegistroBase):
    pass

class Registro(RegistroBase):
    id: int # El ID de la tabla

    class Config:
        from_attributes = True