# Autor: Gabriel Raulino
from typing import Optional, Union, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import date
if TYPE_CHECKING:
    from .cliente import Cliente
    from .funcionario import Funcionario
    from .veiculo import Veiculo
class VendaBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    data: Union[date, None] = None
    valor: float
    vendedor_id: int = Field(foreign_key="funcionario.id")
    cliente_id: int = Field(foreign_key="cliente.id")
    veiculo_id: int = Field(foreign_key="veiculo.id")
class Venda(VendaBase, table=True):
    vendedor: Optional["Funcionario"] = Relationship(back_populates="vendas")
    cliente: Optional["Cliente"] = Relationship(back_populates="vendas")
    veiculo: Optional["Veiculo"] = Relationship(back_populates="vendas")
# Importação atrasada para evitar importação circular
from .funcionario import Funcionario
from .cliente import Cliente