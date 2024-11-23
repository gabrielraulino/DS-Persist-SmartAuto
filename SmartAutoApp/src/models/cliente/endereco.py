"""
Autor: Gabriel Raulino
"""

from typing import Union
import uuid
from pydantic import BaseModel


class Endereco(BaseModel):
    """
    Autor: Gabriel Raulino
    """

    id: Union[uuid.UUID, None] = None
    uf: str
    cidade: str
    logradouro: str
    numero: str
