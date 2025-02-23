from odmantic import Model, Reference, ObjectId
from datetime import date
from typing import  Optional
from models.cliente import Cliente
from models.funcionario import Funcionario
from models.veiculo import Veiculo
class VendaBase(Model):
    data: Optional[date] = None
    valor: float
class Venda(Model):
    data: Optional[date] = None
    valor: float
    vendedor: Funcionario = Reference()
    cliente: Cliente = Reference()
    veiculo_ids: list[ObjectId]

