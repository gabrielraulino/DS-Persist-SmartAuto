"""
Autor: Gabriel Raulino
"""

from sqlmodel import SQLModel, Field


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
