# Autor: Gabriel Raulino

import uuid
import Gerente


class Admin(Gerente):
    def __init__(
        self,
        id: uuid.UUID,
        usuario: str,
        senha: str,
        nome: str,
        telefone: str,
    ):
        super().__init__(id, usuario, senha, nome, telefone)
