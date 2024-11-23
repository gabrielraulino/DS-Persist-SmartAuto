from fastapi import APIRouter, HTTPException
from http import HTTPStatus
import uuid
from typing import List
from datetime import date
from models.locacao import Locacao
from utils.file_handler import read_csv, append_csv, write_csv

locacoes_router = APIRouter()
file = "src/storage/locacoes.csv"
campos = ["id", "data_inicio", "data_fim", "valor_diaria", "cliente_id", "vendedor_id", "veiculo_id",]

locacoes_data = read_csv(file)  # Carrega os dados do arquivo CSV
locacoes: List[Locacao] = [Locacao(**l) for l in locacoes_data]


@locacoes_router.get("/locacoes/", response_model=List[Locacao])
def listar_locacoes():
    return locacoes


@locacoes_router.post("/locacoes/", response_model=Locacao, status_code=HTTPStatus.CREATED)
def criar_locacao(locacao: Locacao):
    if locacao.id is None:
        locacao.id = uuid.uuid4()
    elif any(l.id == locacao.id for l in locacoes):
        raise HTTPException(status_code=400, detail="ID já existe.")
    
    # Adiciona a locação à lista
    locacoes.append(locacao)
    append_csv(file, campos, locacao.dict())
    return locacao


@locacoes_router.get("/locacoes/{id}", response_model=Locacao)
def buscar_locacao(id: uuid.UUID):
    for l in locacoes:
        if l.id == id:
            return l
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Locação não encontrada.")


@locacoes_router.put("/locacoes/{id}", response_model=Locacao)
def atualizar_locacao(id: uuid.UUID, atualizado: Locacao):
    for index, l in enumerate(locacoes):
        if l.id == id:
            if atualizado.id != id:
                atualizado.id = id
            locacoes[index] = atualizado
            write_csv(file, campos, [locacao.dict() for locacao in locacoes])
            return atualizado
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Locação não encontrada.")


@locacoes_router.delete("/locacoes/{id}")
def remover_locacao(id: uuid.UUID):
    for l in locacoes:
        if l.id == id:
            locacoes.remove(l)
            write_csv(file, campos, [locacao.dict() for locacao in locacoes])
            return {"msg": "Locação removida com sucesso!"}
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Locação não encontrada.")
