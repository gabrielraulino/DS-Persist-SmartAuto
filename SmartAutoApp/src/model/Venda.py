# Autor: Gabriel Raulino
from pydantic import BaseModel
import uuid
from datetime import date
from model.Vendedor import Vendedor
from model.Cliente import Cliente
from model.Veiculo import Veiculo


class Venda(BaseModel):
    def __init__(
        self,
        id: uuid.UUID,
        data: date,
        valor: float,
        vendedor: Vendedor,
        cliente: Cliente,
        veiculo: Veiculo,
    ):
        self._id
