from odmantic import Model, Field
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .venda import Venda
    from .locacao import Locacao


class Cliente(Model):
    nome: str
    telefone: str
    email: str
    uf: str
    cidade: str
    logradouro: str
    numero: int
    vendas: Optional[List["Venda"]] = []
    locacoes: Optional[List["Locacao"]] = []

    class Config:
        collection = "clientes"


class ClienteComVendas(Cliente):
    vendas: Optional[List["Venda"]] = []


from .venda import Venda
from .locacao import Locacao
