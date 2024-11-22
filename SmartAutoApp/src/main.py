# imports do fastAPI
from typing import Union
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import uuid

from model.Cliente import Cliente

from model.Funcionario import Funcionario
from model.Endereco import Endereco


vendedores: List[Funcionario] = [
    {
        "id": 1,
        "usuario": "beulah_g",
        "senha": "senha_segura",
        "telefone": "(526) 880-5527",
    },
    {
        "id": 2,
        "usuario": "john_d",
        "senha": "senha_forte",
        "telefone": "(123) 456-7890",
    },
    {
        "id": 3,
        "usuario": "jane_s",
        "senha": "senha_segura123",
        "telefone": "(987) 654-3210",
    },
]


endereco = Endereco(
    id=uuid.uuid4(),
    uf="CE",
    cidade="Fortaleza",
    logradouro="Rua das Flores",
    numero="123",
)
clientes: List[Cliente] = [
    {
        "id": uuid.uuid1(),
        "nome": "joao",
        "telefone": "998876654",
        "email": "example@domain.com",
        "endereco": endereco,
    }
]

app = FastAPI()


@app.get("/")
def read_root():
    return {"msg": "Hello World"}


@app.get("/vendedores/")
def listar_vendedores():
    return vendedores


@app.get("/clientes/")
def listar_clientes():
    return clientes
