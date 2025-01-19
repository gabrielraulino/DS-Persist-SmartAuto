# Autor: Antonio Kleberson
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class CategoriaVeiculo(SQLModel, table=True):
    categoria_id: Optional[int] = Field(default=None, foreign_key="categoria.id", primary_key=True)
    veiculo_id: Optional[int] = Field(default=None, foreign_key="veiculo.id", primary_key=True)

class Categoria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    desc: str
    veiculos: List["Veiculo"] = Relationship(back_populates="categorias", link_model=CategoriaVeiculo)

class Veiculo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    modelo: str
    categorias: List[Categoria] = Relationship(back_populates="veiculos", link_model=CategoriaVeiculo)
