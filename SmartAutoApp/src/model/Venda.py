# Autor: Gabriel Raulino
from pydantic import BaseModel
import uuid
from datetime import date
from model.Funcionario import Funcionario
from model.Cliente import Cliente
from model.Veiculo import Veiculo


class Venda(BaseModel):
    id: uuid.UUID
    data: date
    valor: float
    vendedor: Funcionario
    cliente: Cliente
    veiculo: Veiculo
