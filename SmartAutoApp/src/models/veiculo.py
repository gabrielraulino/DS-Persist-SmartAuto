from typing import Union
from pydantic import BaseModel
import uuid


class Veiculo(BaseModel):
    id: Union[uuid.UUID, None] = None
    marca: str
    modelo: str
    ano: int
    preco: float
    valor_diaria: float
    cor: str
    disponivel: bool
