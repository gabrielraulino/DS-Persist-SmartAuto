"""
Autor: Gabriel Raulino
"""

from fastapi import APIRouter, HTTPException
from http import HTTPStatus
import uuid
from typing import List
from datetime import date
from models.venda import Venda
from utils.file_handler import read_csv, append_csv, write_csv

vendas_router = APIRouter()
file = "src/storage/vendas.csv"
campos = ["id", "data", "valor", "cliente_id", "vendedor_id", "veiculo_id"]

vendas_data = read_csv(file)  # Carrega os dados do arquivo CSV
vendas: List[Venda] = [Venda(**v) for v in vendas_data]


@vendas_router.get("/vendas/", response_model=List[Venda])
def listar_vendas():
    return vendas


@vendas_router.post("/vendas/", response_model=Venda, status_code=HTTPStatus.CREATED)
def criar_venda(venda: Venda):
    if venda.data is None:
        venda.data = date.today()
    if venda.id is None:
        venda.id = uuid.uuid4()
    elif any(v.id == venda.id for v in vendas):
        raise HTTPException(status_code=400, detail="ID já existe.")

    # Adiciona a venda à lista
    vendas.append(venda)
    append_csv(file, campos, venda.model_dump())
    return venda


@vendas_router.get("/vendas/{id}", response_model=Venda)
def buscar_venda(id: uuid.UUID):
    for v in vendas:
        if v.id == id:
            return v
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail="Venda não encontrada."
    )


@vendas_router.put("/vendas/{id}", response_model=Venda)
def atualizar_venda(id: uuid.UUID, atualizado: Venda):
    for index, v in enumerate(vendas):
        if v.id == id:
            if atualizado.id != id:
                atualizado.id = id
            vendas[index] = atualizado
            write_csv(file, campos, [venda.model_dump() for venda in vendas])
            return atualizado
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail="Venda não encontrada."
    )


@vendas_router.delete("/vendas/{id}")
def remover_venda(id: uuid.UUID):
    for v in vendas:
        if v.id == id:
            vendas.remove(v)
            write_csv(file, campos, [venda.model_dump() for venda in vendas])
            return {"msg": "Venda removida com sucesso!"}
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail="Venda não encontrada."
    )
