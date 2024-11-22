# Autor: Gabriel Raulino
from typing import Union
import uuid
from pydantic import BaseModel

from models.endereco import Endereco


class Cliente(BaseModel):
    id: Union[uuid.UUID, None] = None
    nome: str
    telefone: str
    email: str
    endereco: Endereco
