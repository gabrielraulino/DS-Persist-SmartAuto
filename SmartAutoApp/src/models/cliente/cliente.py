"""
Autor: Gabriel Raulino
"""

from typing import Union
import uuid
from pydantic import BaseModel

from models.cliente.endereco import Endereco


class Cliente(BaseModel):
    """
    Autor : Gabriel Raulino
    """

    id: Union[uuid.UUID, None] = None
    nome: str
    telefone: str
    email: str
    endereco: Endereco
