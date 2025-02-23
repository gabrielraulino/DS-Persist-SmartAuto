from datetime import datetime
from typing import Optional
from odmantic import Model, Reference
from models.funcionario import Funcionario
from models.cliente import Cliente
from models.veiculo import Veiculo


class Locacao(Model):
    data_inicio: Optional[datetime] = None
    data_fim: datetime 
    valor_diaria: Optional[float] = None
    cliente: Cliente = Reference()
    vendedor: Funcionario = Reference()
    veiculo: Veiculo = Reference()

