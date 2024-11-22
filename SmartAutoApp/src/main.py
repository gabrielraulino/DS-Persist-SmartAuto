# imports do fastAPI
from http import HTTPStatus
from typing import Union
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from routes.funcionarios import funcionarios_router
from models.cliente import Cliente
from models.endereco import Endereco

from routes.clientes import clientes_router

# from src.routes.funcionario_route import fun
import uuid


app = FastAPI()
# endereco = Endereco(
#     id=uuid.uuid4(),
#     uf="CE",
#     cidade="Fortaleza",
#     logradouro="Rua das Flores",
#     numero="123",
# )

# clientes: List[dict] = [
#     {
#         "id": uuid.uuid1(),
#         "nome": "joao",
#         "telefone": "998876654",
#         "email": "example@domain.com",
#         "endereco": endereco,
#     }
# ]


@app.get("/")
def read_root():
    return {"msg": "Hello World"}


app.include_router(funcionarios_router)
app.include_router(clientes_router)
