# Autor: Gabriel Raulino
from enum import Enum
from odmantic import Model


class Role(str, Enum):
    VENDEDOR = "vendedor"
    GERENTE = "gerente"
    ADMIN = "admin"


class Funcionario(Model):
    nome: str
    usuario: str
    senha: str
    telefone: str
    funcao: Role
