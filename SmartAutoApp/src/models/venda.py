# Autor: Gabriel Raulino
from typing import Union
from pydantic import BaseModel
import uuid
from datetime import date


class Venda(BaseModel):
    id: Union[uuid.UUID, None] = None
    data: Union[date, None] = None
    valor: float
    vendedor_id: uuid.UUID
    cliente_id: uuid.UUID
    veiculo_id: uuid.UUID
