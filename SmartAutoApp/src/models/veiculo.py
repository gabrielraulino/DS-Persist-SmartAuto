from sqlmodel import SQLModel, Field, Relationship


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
    venda_id: int | None = Field(default=None, foreign_key="venda.id")
    categorias: list["Categoria"] = Relationship(link_model=CategoriaVeiculo)
    venda: "Venda" = Relationship(back_populates="veiculos")
    locacoes: list["Locacao"] = Relationship(back_populates="veiculo")


class VeiculoComCategorias(VeiculoBase):
    categorias: list["Categoria"] = []


from models.categoria import Categoria
from models.venda import Venda
from models.locacao import Locacao
