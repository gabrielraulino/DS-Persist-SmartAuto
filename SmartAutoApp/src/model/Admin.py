# Autor: Gabriel Raulino

import uuid
import Gerente
from src.model.Endereco import Endereco


class Admin(Gerente):

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

