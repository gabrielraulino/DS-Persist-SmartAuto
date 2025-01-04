"""
Autor: Gabriel Raulino
"""

from enum import Enum
from typing import Union
import uuid

from pydantic import BaseModel


class Role(str, Enum):
    VENDEDOR = "vendedor"
    GERENTE = "gerente"
    ADMIN = "admin"


class Funcionario(BaseModel):
    """
    Autor: Gabriel Raulino
    """

    id: Union[uuid.UUID, None] = None
    usuario: str
    senha: str
    nome: str
    telefone: str
    funcao: Role

    def __init__(
        self,
        id: Union[uuid.UUID, None],
        usuario: str,
        senha: str,
        nome: str,
        telefone: str,
        funcao: Role,
    ):
        super().__init__(
            id=id,
            usuario=usuario,
            senha=senha,
            nome=nome,
            telefone=telefone,
            funcao=funcao.lower(),
        )
