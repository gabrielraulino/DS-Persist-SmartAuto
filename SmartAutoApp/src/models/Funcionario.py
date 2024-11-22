# Autor: Gabriel Raulino

from enum import Enum
import uuid

from pydantic import BaseModel


class Role(str, Enum):
    VENDEDOR = "vendedor"
    GERENTE = "gerente"
    ADMIN = "admin"


class Funcionario(BaseModel):
    id: int
    usuario: str
    senha: str
    nome: str
    telefone: str
    funcao: Role

    # def inserir_veiculo(self, veiculo: Veiculo) -> None:
    #     # Lógica para inserir um veículo
    #     pass

    # def realizar_venda(self, venda: Venda) -> None:
    #     # Lógica para realizar uma venda
    #     pass

    # def realizar_locacao(self, locacao: Locacao) -> None:
    #     # Lógica para realizar uma locação
    #     pass

    # def inserir_cliente(self, cliente: Cliente) -> None:
    #     pass
