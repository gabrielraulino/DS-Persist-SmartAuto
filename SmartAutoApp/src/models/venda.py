# Autor: Gabriel Raulino
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import date

if TYPE_CHECKING:
    from .cliente import Cliente
    from .funcionario import Funcionario
    from .veiculo import Veiculo


class VendaBase(SQLModel):
    id: int = Field(default=None, primary_key=True)
    data: date | None = None
    valor: float
    vendedor_id: int = Field(foreign_key="funcionario.id")
    cliente_id: int = Field(foreign_key="cliente.id")
    veiculo_id: int = Field(foreign_key="veiculo.id")


class Venda(VendaBase, table=True):
    vendedor: "Funcionario" = Relationship(back_populates="vendas")
    cliente: "Cliente" = Relationship(back_populates="vendas")
    veiculo: "Veiculo" = Relationship(back_populates="vendas")


class VendaComplexa(SQLModel):
    id: int
    data: date | None = None
    valor: float
    vendedor: "Funcionario"
    cliente: "Cliente"
    veiculo: "Veiculo"


from .cliente import Cliente
from .funcionario import Funcionario
from .veiculo import Veiculo
