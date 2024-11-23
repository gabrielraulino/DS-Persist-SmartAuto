from fastapi import APIRouter, HTTPException
from http import HTTPStatus
import uuid
from typing import List
from models.veiculo import Veiculo
from utils.file_handler import read_csv, append_csv, write_csv

veiculos_router = APIRouter()
file = "src/storage/veiculos.csv"
campos = ["id", "marca", "modelo", "ano", "preco", "valor_diaria", "disponivel", "cor"]

veiculos_data = read_csv(file)  # Carrega os dados do arquivo CSV
veiculos: List[Veiculo] = [Veiculo(**v) for v in veiculos_data]


@veiculos_router.get("/veiculos/", response_model=List[Veiculo])
def listar_veiculos():
    return veiculos


@veiculos_router.post("/veiculos/", response_model=Veiculo, status_code=HTTPStatus.CREATED)
def criar_veiculo(veiculo: Veiculo):
    if veiculo.id is None:
        veiculo.id = uuid.uuid4()
    elif any(v.id == veiculo.id for v in veiculos):
        raise HTTPException(status_code=400, detail="ID já existe.")
    
    veiculos.append(veiculo)
    append_csv(file, campos, veiculo.dict())
    return veiculo


@veiculos_router.get("/veiculos/{id}", response_model=Veiculo)
def buscar_veiculo(id: uuid.UUID):
    for v in veiculos:
        if v.id == id:
            return v
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Veículo não encontrado.")


@veiculos_router.put("/veiculos/{id}", response_model=Veiculo)
def atualizar_veiculo(id: uuid.UUID, atualizado: Veiculo):
    for index, v in enumerate(veiculos):
        if v.id == id:
            if atualizado.id != id:
                atualizado.id = id
            veiculos[index] = atualizado
            write_csv(file, campos, [veiculo.dict() for veiculo in veiculos])
            return atualizado
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Veículo não encontrado.")


@veiculos_router.delete("/veiculos/{id}")
def remover_veiculo(id: uuid.UUID):
    for v in veiculos:
        if v.id == id:
            veiculos.remove(v)
            write_csv(file, campos, [veiculo.dict() for veiculo in veiculos])
            return {"msg": "Veículo removido com sucesso!"}
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Veículo não encontrado.")
