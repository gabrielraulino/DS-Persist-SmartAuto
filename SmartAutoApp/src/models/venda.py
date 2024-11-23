# Autor: Gabriel Raulino
from pydantic import BaseModel
import uuid
from datetime import date


class Venda(BaseModel):
    id: uuid.UUID
    data: date
    valor: float
    vendedor: uuid.UUID
    cliente: uuid.UUID
    veiculo: uuid.UUID
