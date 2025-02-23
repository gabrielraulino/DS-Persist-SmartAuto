# Autor: Gabriel Raulino
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date
from bson import ObjectId
from pydantic.networks import EmailStr

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')

class VendaBase(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    data: Optional[date] = None
    valor: float

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

class Venda(VendaBase):
    vendedor_id: PyObjectId
    cliente_id: PyObjectId
    veiculo_ids: List[PyObjectId]

class VendaComplexa(VendaBase):
    vendedor: "Funcionario"
    cliente: "Cliente"
    veiculos: List["Veiculo"]

class Funcionario(BaseModel):
    id: PyObjectId
    nome: str
    email: EmailStr

class Cliente(BaseModel):
    id: PyObjectId
    nome: str
    email: EmailStr

class Veiculo(BaseModel):
    id: PyObjectId
    modelo: str
    marca: str
    ano: int
