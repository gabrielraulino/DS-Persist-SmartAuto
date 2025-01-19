# Autor: Antonio Kleberson
from sqlmodel import SQLModel, Field, Relationship
from .venda import VendaBase


class VeiculoBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    marca: str
    modelo: str
    ano: int
    preco: float
    cor: str
    disponivel: bool

class Veiculo(VeiculoBase, table=True):
    venda_id: int = Field(foreign_key="venda.id")
    venda: 'VendaBase' =  Relationship(back_populates="vendas")