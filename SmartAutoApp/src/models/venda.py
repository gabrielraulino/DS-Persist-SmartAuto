# Autor: Gabriel Raulino
from typing import Optional, Union
from sqlmodel import SQLModel, Field, Relationship
from datetime import date

class VendaBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    data: Union[date, None] = None
    valor: float
    vendedor_id: int = Field(foreign_key="funcionario.id")

class Venda(VendaBase, table=True):
    vendedor: Optional["Funcionario"] = Relationship(back_populates="vendas")

# Importação atrasada para evitar importação circular
from .funcionario import Funcionario