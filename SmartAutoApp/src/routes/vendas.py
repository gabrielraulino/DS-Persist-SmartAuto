"""
Autor: Gabriel Raulino
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from http import HTTPStatus
from sqlmodel import Session, select
from database.database import get_session  
from models.venda import Venda, VendaCreate, VendaUpdate  
from typing import List

router = APIRouter(prefix="/vendas", tags=["Vendas"])
file = "src/storage/vendas.csv"
campos = [
    "id",
    "valor",
    "cliente_id",
    "vendedor_id",
    "veiculo_id",
]

locacoes_data = read_csv(file)  # Carrega os dados do arquivo CSV


@router.get("/")
def litar():
    if locacoes_data.empty:
        return []
    return locacoes_data.to_dict(orient="records")


@router.post("/", response_model=Venda, status_code=HTTPStatus.CREATED)
def criar_venda(venda: VendaCreate, session: Session = Depends(get_session)):
    nova_venda = Venda(**venda.dict())
    session.add(nova_venda)
    session.commit()
    session.refresh(nova_venda)
    return nova_venda.model_dump()

@router.get("/{id}", response_model=Venda)
def buscar(id: uuid.UUID):
    global locacoes_data
    if locacoes_data.empty:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Lista Vazia")
    venda = locacoes_data[locacoes_data["id"] == str(id)]
    if venda.empty:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Locação não encontrada."
        )
    return venda.to_dict(orient="records")[0]


@router.put("/{id}", response_model=Venda)
def atualizar(id: uuid.UUID, atualizado: Venda):
    global locacoes_data
    if locacoes_data.empty:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Vazio.")
    if atualizado.id == None:
        atualizado.id = id
    venda = locacoes_data[locacoes_data["id"] == str(id)]
    if venda.empty:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Venda não encontrada."
        )
    locacoes_data.loc[venda.index[0]] = atualizado.model_dump()
    locacoes_data.to_csv(file, index=False)
    return atualizado


@router.delete("/{id}")
def remover(id: uuid.UUID):
    global locacoes_data
    if locacoes_data.empty:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Não existe nenhuma Venda."
        )
    venda = locacoes_data[locacoes_data["id"] == str(id)]
    if venda.empty:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Venda não encontrada."
        )
    locacoes_data = locacoes_data.drop(venda.index[0])
    locacoes_data.to_csv(file, index=False)
    return {"Venda apaga com sucesso"}
