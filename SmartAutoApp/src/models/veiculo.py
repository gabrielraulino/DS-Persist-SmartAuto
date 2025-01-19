# Autor: Antonio Kleberson
from typing import TYPE_CHECKING, Union
from sqlmodel import SQLModel, Field


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
    categoria_id: int | None = Field(default=None, foreign_key="categoria.id")