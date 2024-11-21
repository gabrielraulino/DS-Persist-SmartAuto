import uuid
from datetime import date
import Endereco
# from typing import List


class Vendedor:
    def __init__(self, id: uuid.UUID, usuario: str, senha: str, nome: str, telefone: str, endereco: Endereco):
        self._id = id
        self._usuario = usuario
        self._senha = senha
        self._nome = nome
        self._telefone = telefone
        self._endereco = endereco

    #     self._endereco = endereco

    # def __init__(self, id: uuid.UUID, usuario: str, senha: str, nome: str):
    #     self._id = id
    #     self._usuario = usuario
    #     self._senha = senha
    #     self._nome = nome

    # def inserir_veiculo(self, veiculo : Veiculo) -> None:
    #     # Lógica para inserir um veículo
    #     pass

    # def realizar_venda(self, venda: Venda) -> None:
    #     # Lógica para realizar uma venda
    #     pass

    # def realizar_locacao(self, locacao: Locacao) -> None:
    #     # Lógica para realizar uma locação
    #     pass
    # def inserir_cliente(self, cliente: Locacao) -> None:
    #     pass

# Exemplo de uso da classe
# if __name__ == "__main__":
#     vendedor_id = uuid.uuid4()
#     vendedor = Vendedor(id=vendedor_id, usuario="vendedor123", senha="senha_segura", nome="João Silva")
#     print(f"Vendedor criado: {vendedor._nome} (ID: {vendedor._id})")

