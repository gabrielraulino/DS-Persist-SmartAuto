"""
Autor: Gabriel Raulino
"""

from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field

if TYPE_CHECKING:
    from .venda import Venda

class Cliente(SQLModel, table=True):
    """
    Autor : Gabriel Raulino
    """

    id: int | None = Field(default=None, primary_key=True)
    nome: str
    telefone: str
    email: str
    uf: str
    cidade: str
    logradouro: str
    numero: int
    vendas: list["Venda"] = Field(default_factory=list, sa_relationship_kwargs={"back_populates": "cliente"})
