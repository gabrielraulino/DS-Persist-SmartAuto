from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .veiculo import Veiculo


class Categoria(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    desc: str
