# Autor: Gabriel Raulino
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum


class Role(str, Enum):
    VENDEDOR = "vendedor"
    GERENTE = "gerente"
    ADMIN = "admin"


class FuncionarioBase(SQLModel):
    id: int = Field(default=None, primary_key=True)
    usuario: str
    senha: str
    nome: str
    telefone: str
    funcao: Role


class Funcionario(FuncionarioBase, table=True):
    vendas: list["Venda"] = Relationship(back_populates="vendedor")
    locacoes: list["Locacao"] = Relationship(back_populates="vendedor")


from .venda import Venda
from .locacao import Locacao
