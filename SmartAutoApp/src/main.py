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


@app.get("/")
def read_root():
    return {"msg": "SmartAutoApp"}


app.include_router(funcionarios_router)
app.include_router(clientes_router)
