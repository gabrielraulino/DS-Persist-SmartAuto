# Autor: Gabriel Raulino
from pydantic import BaseModel
import uuid
from datetime import date
from models.funcionario import Funcionario
from models.cliente import Cliente
from models.veiculo import Veiculo


class Venda(BaseModel):
    id: uuid.UUID
    data: date
    valor: float
    vendedor: Funcionario
    cliente: Cliente
    veiculo: Veiculo
