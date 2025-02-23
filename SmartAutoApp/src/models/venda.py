from odmantic import Model, Field, Reference, ObjectId
from datetime import date
from typing import List, Optional
from pydantic.networks import EmailStr

class Funcionario(Model):
    nome: str
    email: EmailStr

class Cliente(Model):
    nome: str
    email: EmailStr

class Veiculo(Model):
    modelo: str
    marca: str
    ano: int

class VendaBase(Model):
    data: Optional[date] = None
    valor: float

class Venda(VendaBase):
    # Armazena apenas os ObjectId das referências
    vendedor_id: ObjectId
    cliente_id: ObjectId
    veiculo_ids: List[ObjectId]

class VendaComplexa(VendaBase):
    # Utiliza referências para armazenar os documentos completos
    vendedor: Funcionario = Reference()
    cliente: Cliente = Reference()
    veiculos: List[Veiculo] = Field(default_factory=list)
