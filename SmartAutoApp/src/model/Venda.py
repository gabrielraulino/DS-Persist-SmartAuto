# Autor: Gabriel Raulino
from pydantic import BaseModel
import uuid
from datetime import date
from src.model.Vendedor import Vendedor
from src.model.Cliente import Cliente
from src.model.Veiculo import Veiculo


class Venda(BaseModel):
    def __init__(
        self,
        id: uuid.UUID,
        data: date,
        valor: float,
        vendedor: Vendedor,
        cliente: Cliente,
    ):
        self._id
