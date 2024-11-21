import uuid


class Endereco:
    def __init__(
        self, id: uuid.UUID, uf: str, cidade: str, logradouro: str, numero: str
    ) -> None:
        self._id = id
        self._uf = uf
        self._cidade = cidade
        self._logradouro = logradouro
        self._numero = numero

    def __str__(self):
        return f"{self._logradouro}, {self._numero} - {self._cidade}/{self._uf}"
