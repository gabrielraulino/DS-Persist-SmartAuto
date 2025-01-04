from fastapi import APIRouter, HTTPException
from http import HTTPStatus
import uuid
from models.veiculo import Veiculo
from utils.file_handler import read_csv, append_csv

veiculos_router = APIRouter(prefix="/veiculos", tags=["Veiculos"])
file = "src/storage/veiculos.csv"
campos = ["id", "marca", "modelo", "ano", "preco", "valor_diaria", "disponivel", "cor"]

veiculos_data = read_csv(file)  # Carrega os dados do arquivo CSV


@veiculos_router.get("/")
def listar():
    if veiculos_data.empty:
        return []
    return veiculos_data.to_dict(orient="records")


@veiculos_router.post("/", response_model=Veiculo, status_code=HTTPStatus.CREATED)
def criar(veiculo: Veiculo):
    global veiculos_data
    if veiculo.id is None:
        veiculo.id = uuid.uuid4()
    elif not veiculos_data[veiculos_data["id"] == veiculo.id].empty:
        raise HTTPException(status_code=400, detail="ID já existe.")
    veiculo_validado = Veiculo.model_validate(veiculo)
    veiculo_validado = Veiculo.par
    veiculos_data = append_csv(
        file, campos, veiculo_validado.model_dump(), veiculos_data
    )
    return veiculo_validado


@veiculos_router.get("/{id}", response_model=Veiculo)
def buscar(id: str):
    global veiculos_data
    veiculo = veiculos_data[veiculos_data["id"] == id]
    if veiculo.empty:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Veículo não encontrado."
        )
    return veiculo.to_dict(orient="records")[0]


@veiculos_router.put("/{id}", response_model=Veiculo)
def atualizar(id: str, veiculo: Veiculo):
    global veiculos_data
    elemento = veiculos_data[veiculos_data["id"] == id]
    if elemento.empty:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Veículo não encontrado."
        )
    if veiculo.id is None:
        veiculo.id = id
    veiculo_validado = Veiculo.model_validate(veiculo)
    veiculos_data.loc[elemento.index[0]] = veiculo_validado.model_dump()
    veiculos_data.to_csv(file, index=False)
    return veiculo_validado


@veiculos_router.delete("/{id}")
def remover(id: str):
    global veiculos_data
    elemento = veiculos_data[veiculos_data["id"] == id]
    if elemento.empty:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Veículo não encontrado."
        )
    index = elemento.index[0]
    veiculos_data = veiculos_data.drop(index)
    veiculos_data.to_csv(file, index=False)
    return {"detail": "Veículo excluído com sucesso"}
