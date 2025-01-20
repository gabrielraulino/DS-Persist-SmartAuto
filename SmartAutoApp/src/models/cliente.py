from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

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
    vendas: List["Venda"] = Relationship(back_populates="cliente")