from odmantic import Model, Reference
from datetime import datetime
from typing import  Optional
from models.cliente import Cliente
from models.funcionario import Funcionario
from models.veiculo import Veiculo

class Venda(Model):
    data: Optional[datetime] = None
    valor: float
    vendedor: Funcionario = Reference()
    cliente: Cliente = Reference()
    veiculo: Veiculo = Reference()

