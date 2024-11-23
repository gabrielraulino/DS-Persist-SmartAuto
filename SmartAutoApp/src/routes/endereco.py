from fastapi import APIRouter, HTTPException
from http import HTTPStatus
import uuid
from typing import List
from models.cliente.endereco import Endereco
from utils.file_handler import read_csv, append_csv, write_csv

enderecos_router = APIRouter()
file = "src/storage/enderecos.csv"
campos = ["id", "uf", "cidade", "logradouro", "numero"]

enderecos_data = read_csv(file)  # Carrega os dados do arquivo CSV
enderecos: List[Endereco] = [Endereco(**e) for e in enderecos_data]


@enderecos_router.get("/enderecos/", response_model=List[Endereco])
def listar_enderecos():
    return enderecos


@enderecos_router.post(
    "/enderecos/", response_model=Endereco, status_code=HTTPStatus.CREATED
)
def criar_endereco(endereco: Endereco):
    if endereco.id is None:
        endereco.id = uuid.uuid4()
    elif any(e.id == endereco.id for e in enderecos):
        raise HTTPException(status_code=400, detail="ID já existe.")

    enderecos.append(endereco)
    append_csv(file, campos, endereco.dict())
    return endereco


@enderecos_router.get("/enderecos/{id}", response_model=Endereco)
def buscar_endereco(id: uuid.UUID):
    for e in enderecos:
        if e.id == id:
            return e
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail="Endereço não encontrado."
    )


@enderecos_router.put("/enderecos/{id}", response_model=Endereco)
def atualizar_endereco(id: uuid.UUID, atualizado: Endereco):
    for index, e in enumerate(enderecos):
        if e.id == id:
            if atualizado.id != id:
                atualizado.id = id
            enderecos[index] = atualizado
            write_csv(file, campos, [endereco.dict() for endereco in enderecos])
            return atualizado
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail="Endereço não encontrado."
    )


@enderecos_router.delete("/enderecos/{id}")
def remover_endereco(id: uuid.UUID):
    for e in enderecos:
        if e.id == id:
            enderecos.remove(e)
            write_csv(file, campos, [endereco.dict() for endereco in enderecos])
            return {"msg": "Endereço removido com sucesso!"}
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail="Endereço não encontrado."
    )
