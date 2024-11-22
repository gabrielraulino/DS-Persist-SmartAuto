# Autor: Gabriel Raulino
import uuid
from pydantic import BaseModel

from models.endereco import Endereco


class Cliente(BaseModel):
    id: uuid.UUID
    nome: str
    telefone: str
    email: str
    endereco: Endereco
