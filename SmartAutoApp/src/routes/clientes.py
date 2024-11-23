"""
Autor : Gabriel Raulino
"""

from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from typing import List
from uuid import UUID
import uuid
from models.cliente.cliente import Cliente
from models.cliente.endereco import Endereco
from utils.file_handler import read_csv, append_csv, write_csv

clientes_router = APIRouter()
file = "src/storage/clientes.csv"
campos = ["id", "nome", "telefone", "email", "endereco"]
clientes_data = read_csv(file)
# clientes: List[Cliente] = [Cliente(**c) for c in clientes_data]

clientes: List[Cliente] = []
for c in clientes_data:
    try:
        # Verifica se o campo 'endereco' é uma string e tenta convertê-lo em um dicionário
        if isinstance(c["endereco"], str):
            c["endereco"] = eval(c["endereco"])

        # Se o campo 'endereco' for um dicionário válido, converte-o para uma instância de Endereco
        if isinstance(c["endereco"], dict):
            c["endereco"] = Endereco(**c["endereco"])

        # Adiciona à lista de clientes como uma instância de Cliente
        clientes.append(Cliente(**c))
    except (SyntaxError, TypeError, ValueError) as e:
        # Caso ocorra um erro de conversão, ignora o cliente atual e continua
        print(f"Erro ao converter o endereço do cliente com ID {c.get('id')}: {e}")


@clientes_router.get("/clientes/")
def listar_clientes():
    return clientes


@clientes_router.post(
    "/clientes/", response_model=Cliente, status_code=HTTPStatus.CREATED
)
def insere_cliente(cliente: Cliente):
    # Verifica se id de cliente e endereco é não nulo, caso for, faz atribuição automática
    if cliente.endereco.id == None:
        cliente.endereco.id = uuid.uuid4()
    if cliente.id == None:
        cliente.id = uuid.uuid4()
    elif any(c.id == cliente.id for c in clientes):
        raise HTTPException(status_code=400, detail="ID já existe.")
    clientes.append(cliente)

    append_csv(file, campos, cliente.model_dump())
    return cliente


@clientes_router.get("/clientes/{id}")
def buscar_cliente(id: uuid.UUID):
    for cliente_atual in clientes:
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
            write_csv(file, campos, [cliente.model_dump() for cliente in clientes])
            return atualizado
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail="Cliente não encontrado."
    )


@clientes_router.delete("/clientes/{id}")
def remover_cliente(id: uuid.UUID):
    for c in clientes:
        if c.id == id:
            clientes.remove(c)
            write_csv(file, campos, [cliente.model_dump() for cliente in clientes])
            return {"msg": "cliente removido com sucesso!"}
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail="Cliente não encontrado."
    )
