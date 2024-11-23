from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from typing import List
import uuid
from models.cliente import Cliente


clientes_router = APIRouter()
clientes: List[Cliente] = []


@clientes_router.get("/clientes/")
def listar_clientes():
    return clientes


@clientes_router.post(
    "/clientes/", response_model=Cliente, status_code=HTTPStatus.CREATED
)
def insere_cliente(cliente: Cliente):
    if cliente.endereco.id == None:
        cliente.endereco.id = uuid.uuid4()
    if cliente.id == None:
        cliente.id = uuid.uuid4()
    elif any(c.id == cliente.id for c in clientes):
        raise HTTPException(status_code=400, detail="ID já existe.")
    # Verifica se id de cliente e endereco é não nulo
    clientes.append(cliente)
    return cliente


@clientes_router.get("/clientes/{id}")
def buscar_cliente(id: uuid.UUID):
    for indice, cliente_atual in enumerate(clientes):
        if cliente_atual.id == id:
            return cliente_atual
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail="Cliente não encontrado."
    )


@clientes_router.put("/clientes/{id}")
def atualizar_cliente(id: uuid.UUID, atualizado: Cliente):
    for index, c in enumerate(clientes):
        if c.id == id:
            if atualizado.id != id:
                atualizado.id = id
            clientes[index] = atualizado
            return atualizado
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail="Cliente não encontrado."
    )


@clientes_router.delete("/clientes/{id}")
def remover_cliente(id: uuid.UUID):
    for c in clientes:
        if c.id == id:
            clientes.remove(c)
            return {"msg": "cliente removido com sucesso!"}
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail="Cliente não encontrado."
    )
