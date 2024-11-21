import uuid
import Gerente
# import Endereco

class Admin(Gerente):
  # def __init__(self, id: uuid.UUID, usuario: str, senha: str, nome: str, endereco: Endereco):
  #   super().__init__(id, usuario, senha, nome, endereco)

  def __init__(self, id: uuid.UUID, usuario: str, senha: str, nome: str):
    super().__init__(id, usuario, senha, nome)
