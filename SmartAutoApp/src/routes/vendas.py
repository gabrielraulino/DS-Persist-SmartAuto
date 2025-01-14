"""
Autor: Gabriel Raulino
"""

from fastapi import APIRouter, HTTPException
from http import HTTPStatus
import uuid
from models.venda import Venda
from utils.file_handler import read_csv, append_csv

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
def criar(venda: Venda):
    global locacoes_data
    if venda.id is None:
        venda.id = uuid.uuid4()
    elif (
        "id" in locacoes_data.columns
        and not locacoes_data[locacoes_data["id"] == str(venda.id)].empty
    ):
        raise HTTPException(status_code=400, detail="ID já existe.")
    locacoes_data = append_csv(file, campos, venda.model_dump(), locacoes_data)
    return venda


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
