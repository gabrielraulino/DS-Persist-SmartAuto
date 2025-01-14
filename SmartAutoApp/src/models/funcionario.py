"""
Autor: Gabriel Raulino
"""

from enum import Enum
from sqlmodel import SQLModel, Field


class Role(str, Enum):
    VENDEDOR = "vendedor"
    GERENTE = "gerente"
    ADMIN = "admin"


class Funcionario(SQLModel, table=True):
    """
    Autor: Gabriel Raulino
    """

    id: int | None = Field(default=None, primary_key=True)
    usuario: str
    senha: str
    nome: str
    telefone: str
    funcao: Role
