from http import HTTPStatus
from fastapi import APIRouter, HTTPException
import uuid
from typing import List
from models.funcionario import Funcionario, Role
from utils.file_handler import read_csv, append_csv, write_csv

funcionarios_router = APIRouter()
file = "src/storage/funcionarios.csv"
campos = ["id", "usuario", "senha", "nome", "telefone", "funcao"]

funcionarios_data = read_csv(file)  # funcionarios_data recebe um dict
funcionarios: List[Funcionario] = [Funcionario(**f) for f in funcionarios_data]


@funcionarios_router.get("/funcionarios/")
def listar_clientes():
    return funcionarios


@funcionarios_router.post(
    "/funcionarios/", response_model=Funcionario, status_code=HTTPStatus.CREATED
)
def inserir(funcionario: Funcionario):
    try:
        role = Role(funcionario.funcao.lower())
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Função inválida. Valores permitidos: 'vendedor', 'gerente', 'admin'.",
        )
    funcionario.funcao = role
    if funcionario.id == None:
        funcionario.id = uuid.uuid4()
    elif any(f.id == funcionario.id for f in funcionarios):
        raise HTTPException(status_code=400, detail="ID já existe.")
    # Verifica se id de funcionario e endereco é não nulo
    funcionarios.append(funcionario)
    append_csv(file, campos, funcionario.model_dump())
    return funcionario


@funcionarios_router.get("/funcionarios/{id}")
def buscar(id: uuid.UUID):
    # for cliente_atual in funcionarios:
    for f in funcionarios:
        if f.id == id:
            return f
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
            write_csv(
                file, campos, [funcionario.model_dump() for funcionario in funcionarios]
            )
            return atualizado
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail="Funcionário não encontrado."
    )


@funcionarios_router.delete("/funcionarios/{id}")
def remover(id: uuid.UUID):
    for f in funcionarios:
        if f.id == id:
            funcionarios.remove(f)
            write_csv(
                file, campos, [funcionario.model_dump() for funcionario in funcionarios]
            )
            return {"msg": "cliente removido com sucesso!"}
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail="Funcionário não encontrado."
    )
