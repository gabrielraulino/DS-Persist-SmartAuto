from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .venda import Venda


class ClienteBase(SQLModel):
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


class Cliente(ClienteBase, table=True):
    vendas: list["Venda"] = Relationship(back_populates="cliente")


class ClienteComVendas(ClienteBase):
    vendas: list["Venda"]


from .venda import Venda
