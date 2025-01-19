# Autor: Antonio Kleberson
from sqlmodel import SQLModel, Field


class Categoria(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    desc: str

class CategoriaVeiculo(SQLModel, table=True):
    categoria_id = Field(default=None, foreign_key="categoria.id", primary_key=True)
    veiculo_id = Field(default=None, foreign_key="veiculo.id", primary_key=True)
