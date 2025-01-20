# Autor: Gabriel Raulino
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

if TYPE_CHECKING:
    from .venda import Venda


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


# Importação atrasada para evitar importação circular
from .venda import Venda
