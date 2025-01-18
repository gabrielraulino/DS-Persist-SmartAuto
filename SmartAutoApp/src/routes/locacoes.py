from fastapi import APIRouter, HTTPException
from http import HTTPStatus
import uuid
from typing import List
from datetime import date
from models.locacao import Locacao
from utils.file_handler import read_csv, append_csv

router = APIRouter(prefix="/locacoes", tags=["Locacoes"])
file = "src/storage/locacoes.csv"
campos = [
    "id",
    "data_inicio",
    "data_fim",
    "valor_diaria",
    "cliente_id",
    "vendedor_id",
    "veiculo_id",
]

locacoes_data = read_csv(file)  # Carrega os dados do arquivo CSV


@router.get("/")
def listar():
    if locacoes_data.empty:
        return []
    return locacoes_data.to_dict(orient="records")


@router.post("/", response_model=Locacao, status_code=HTTPStatus.CREATED)
def criar(locacao: Locacao):
    global locacoes_data
    if locacao.id is None:
        locacao.id = uuid.uuid4()
    elif (
        "id" in locacoes_data.columns
        and not locacoes_data[locacoes_data["id"] == str(locacao.id)].empty
    ):
        raise HTTPException(status_code=400, detail="ID já existe.")
    # locacao_validado = Locacao.model_validate(locacao)
    locacoes_data = append_csv(file, campos, locacao.model_dump(), locacoes_data)
    return locacao


@locacoes_router.get("/{id}", response_model=Locacao)
def buscar_por_id(id: uuid.UUID):
    global locacoes_data
    if locacoes_data.empty:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Lista Vazia")
    locacao = locacoes_data[locacoes_data["id"] == id]
    if locacao.empty:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Locação não encontrada."
        )
    return locacao.to_dict(orient="records")[0]


@locacoes_router.put("/{id}", response_model=Locacao)
def atualizar(id: uuid.UUID, atualizado: Locacao):
    global locacoes_data
    if locacoes_data.empty:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Vazio.")
    if atualizado.id == None:
        atualizado.id = id
    locacao = locacoes_data[locacoes_data["id"] == str(id)]
    if locacao.empty:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Locação não encontrada."
        )
    locacoes_data.loc[locacao.index[0]] = atualizado.model_dump()
    locacoes_data.to_csv(file, index=False)
    return atualizado


@locacoes_router.delete("/{id}")
def remover(id: uuid.UUID):
    global locacoes_data
    if locacoes_data.empty:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Não existe nenhuma locação."
        )
    locacao = locacoes_data[locacoes_data["id"] == id]
    if locacao.empty:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Locação não encontrada."
        )
    locacoes_data = locacoes_data.drop(locacao.index[0])
    locacoes_data.to_csv(file, index=False)
    return {"Locação apaga com sucesso"}
