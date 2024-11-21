import uuid
import Vendedor
from src.model.Endereco import Endereco


class Gerente(Vendedor):
    def __init__(
        self, 
        id: uuid.UUID, 
        usuario: str, 
        senha: str, nome: 
        str, 
        endereco: Endereco
    ):
        super().__init__(
          id, 
          usuario, 
          senha, 
          nome, 
          endereco
        )

    def inserir_vendedor(self, vendedor: Vendedor) -> None:
        # Lógica para inserir um novo vendedor (ex: salvar em um arquivo CSV)
        pass
