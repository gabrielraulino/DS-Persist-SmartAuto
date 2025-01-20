from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .veiculo import Veiculo

class Categoria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    desc: str
    veiculos: Optional[List["Veiculo"]] = Relationship(back_populates="categoria")
