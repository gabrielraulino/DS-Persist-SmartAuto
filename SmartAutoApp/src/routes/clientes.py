from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from uuid import UUID
from typing import List
from models.cliente import Cliente
from models.endereco import Endereco

# from storage.file_handler import append_csv, read_csv
import pandas as pd
import uuid

clientes_router = APIRouter()
# cliente_csv = "./src/storage/clientes.csv"
clientes: List[Cliente] = []


@clientes_router.get("/clientes/")
def listar_clientes():
    return clientes


@clientes_router.post(
    "/clientes/", response_model=Cliente, status_code=HTTPStatus.CREATED
)
def insere_cliente(cliente: Cliente):
    if any(c.id == cliente.id for c in clientes):
        raise HTTPException(status_code=400, detail="ID já existe.")
    cliente.id = uuid.uuid4()
    cliente.endereco.id = uuid.uuid4()
    clientes.append(cliente)
    return cliente


@clientes_router.get("/clientes/{cliente_id}")
def buscar_cliente(cliente_id: uuid.UUID):
    for indice, cliente_atual in enumerate(clientes):
        if cliente_atual.id == cliente_id:
            return cliente_atual
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Item não encontrado.")


# Persistência dos clientes utilizando armazenamento em CSV
