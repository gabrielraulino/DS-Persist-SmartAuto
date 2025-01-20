from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
if TYPE_CHECKING:
    from .categoria import Categoria
class Veiculo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    marca: str
    modelo: str
    ano: int
    preco: float
    cor: str
    disponivel: bool
    categoria_id: int = Field(foreign_key="categoria.id")
    categoria: Optional["Categoria"] = Relationship(back_populates="veiculos")