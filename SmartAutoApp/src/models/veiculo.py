from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from models.venda import Venda
    from .categoria import Categoria

from enum import Enum


class Ordem(str, Enum):
    ASC: str = "asc"
    DESC: str = "desc"


class CategoriaVeiculo(SQLModel, table=True):
    categoria_id: int = Field(
        default=None, foreign_key="categoria.id", primary_key=True
    )
    veiculo_id: int = Field(default=None, foreign_key="veiculo.id", primary_key=True)


class VeiculoBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    marca: str
    modelo: str
    ano: int
    preco: float
    cor: str
    disponivel: bool


class Veiculo(VeiculoBase, table=True):
    categorias: list["Categoria"] = Relationship(link_model=CategoriaVeiculo)
    vendas: list["Venda"] = Relationship(back_populates="veiculo")


class VeiculoComCategorias(VeiculoBase):
    categorias: list["Categoria"] = []
