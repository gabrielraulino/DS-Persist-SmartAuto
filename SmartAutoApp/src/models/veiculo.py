from typing import Union
from sqlmodel import SQLModel, Field


class Veiculo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    marca: str
    modelo: str
    ano: int
    preco: float
    cor: str
    disponivel: bool
