# Autor: Antonio Kleberson
from typing import TYPE_CHECKING, Union
from sqlmodel import Relationship, SQLModel, Field
from datetime import date

#Relacionamento com cliente

if TYPE_CHECKING:
    from .cliente import Cliente

class Venda(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    data: Union[date, None] = None
    valor: float
    vendedor_id: int
    veiculo_id: int
    cliente_id: int = Field(foreign_key="cliente.id")
    cliente: "Cliente" = Relationship(back_populates="vendas")