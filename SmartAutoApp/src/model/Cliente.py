# Autor: Gabriel Raulino
import uuid
from pydantic import BaseModel
from model.Endereco import Endereco


class Cliente(BaseModel):
    def __init__(
        self, id: uuid.UUID, nome: str, telefone: str, email: str, endereco: Endereco
    ) -> None:
        self._id = id
        self._nome = nome
        self._telefone = telefone
        self._email = email
        self._endereco = endereco

    def __str__(self):
        return f"Cliente(id={self._id}, nome={self._nome}, telefone={self._telefone}, email={self._email}, endereco={self._endereco})"
