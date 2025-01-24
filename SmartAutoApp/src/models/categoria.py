from typing import TYPE_CHECKING
from sqlmodel import Relationship, SQLModel, Field

if TYPE_CHECKING:
    from .veiculo import Veiculo


class Categoria(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nome: str
    desc: str
    veiculos: list["Veiculo"] = Relationship(back_populates="categoria")
