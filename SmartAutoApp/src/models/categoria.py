# Autor: Antonio Kleberson
from sqlmodel import SQLModel, Field
from typing import TYPE_CHECKING, List, Optional
from .veiculo import Veiculo

if TYPE_CHECKING:
    from .veiculo import Veiculo
    
class Categoria(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    desc: str
    veiculos: Optional[List["Veiculo"]] = Field(default=None, sa_relationship_kwargs={"back_populates": "categoria"})
