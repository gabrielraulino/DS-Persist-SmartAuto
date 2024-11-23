#Autor: Antonio Kleberson
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
import uuid

class Locacao(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    data_inicio: date
    data_fim: date
    valor_diaria: float
    cliente_id: uuid.UUID
    vendedor_id: uuid.UUID
    veiculo_id: uuid.UUID

