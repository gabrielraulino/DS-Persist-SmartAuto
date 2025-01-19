# Autor: Gabriel Raulino
from typing import Union
from sqlmodel import Relationship, SQLModel, Field
from datetime import date
from .veiculo import VeiculoBase


class VendaBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    data: Union[date, None] = None
    valor: float
    vendedor_id: int
    cliente_id: int

class VendaBase(VendaBase, table=True):
    veiculos: list[VeiculoBase] = Relationship(back_populates="venda")
