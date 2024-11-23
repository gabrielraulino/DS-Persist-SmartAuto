from http import HTTPStatus
from fastapi import APIRouter, HTTPException
import uuid
from typing import List
from SmartAutoApp.src.models.funcionario import Funcionario, Role


# from storage.file_handler import append_csv, read_csv
import uuid

funcionarios_router = APIRouter()

funcionarios: List[Funcionario] = []


@funcionarios_router.get("/funcionarios/")
def listar_clientes():
    return funcionarios


@funcionarios_router.post(
    "/funcionarios/", response_model=Funcionario, status_code=HTTPStatus.CREATED
)
def inserir(funcionario: Funcionario):
    if funcionario.endereco.id == None:
        funcionario.endereco.id = uuid.uuid4()
    if funcionario.id == None:
        funcionario.id = uuid.uuid4()
    elif any(f.id == funcionario.id for f in funcionarios):
        raise HTTPException(status_code=400, detail="ID já existe.")
    # Verifica se id de funcionario e endereco é não nulo
    funcionarios.append(funcionario)
    return funcionario


@funcionarios_router.get("/funcionarios/{id}")
def buscar(id: uuid.UUID):
    for indice, cliente_atual in enumerate(funcionarios):
        if cliente_atual.id == id:
            return cliente_atual
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail="Funcionário não encontrado."
    )


@funcionarios_router.put("/funcionarios/{id}")
def atualizar(id: uuid.UUID, atualizado: Funcionario):
    for index, f in enumerate(funcionarios):
        if f.id == id:
            if atualizado.id != id:
                atualizado.id = id
            funcionarios[index] = atualizado
            return atualizado
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail="Funcionário não encontrado."
    )


@funcionarios_router.delete("/funcionarios/{id}")
def remover(id: uuid.UUID):
    for f in funcionarios:
        if f.id == id:
            funcionarios.remove(f)
            return {"msg": "cliente removido com sucesso!"}
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail="Funcionário não encontrado."
    )
