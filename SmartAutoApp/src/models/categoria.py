from odmantic import Model, Field
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .veiculo import Veiculo

class Categoria(Model):
    nome: str
    desc: str
    veiculos: Optional[List["Veiculo"]] = []

    class Config:
        collection = "categorias"

class Veiculo(Model):
    nome: str
    categoria_id: str

    class Config:
        collection = "veiculos"
