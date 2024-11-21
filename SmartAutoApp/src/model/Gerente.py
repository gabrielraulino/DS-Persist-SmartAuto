import uuid
import Vendedor


class Gerente(Vendedor):
    def __init__(
        self,
        id: uuid.UUID,
        usuario: str,
        senha: str,
        nome: str,
        telefone: str,
    ):
        super().__init__(id, usuario, senha, nome, telefone)

    def inserir_vendedor(self, vendedor: Vendedor) -> None:
        # Lógica para inserir um novo vendedor (ex: salvar em um arquivo CSV)
        pass
