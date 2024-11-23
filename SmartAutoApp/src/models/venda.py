# Autor: Gabriel Raulino
from typing import Union
from pydantic import BaseModel
import uuid
from datetime import date


class Venda(BaseModel):
    id: Union[uuid.UUID, None] = None
    data: Union[date, None] = None
    valor: float
    vendedor: uuid.UUID
    cliente: uuid.UUID
    veiculo: uuid.UUID
