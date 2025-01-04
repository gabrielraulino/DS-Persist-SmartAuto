from http import HTTPStatus
from fastapi import APIRouter, HTTPException
import uuid
from utils.file_handler import read_csv, append_csv
from utils.zip_handler import compactar_csv
from utils.hash_handler import calcular_hash_sha256
from models.modelo import Modelo

modelos_router = APIRouter(prefix="/modelos", tags=["Modelos"])
campos = ["id", "nome"]
file = "src/storage/modelos.csv"
modelo_data = read_csv(file)


@modelos_router.get("/zip")
def gerar_zip():
    return compactar_csv(file)


@modelos_router.get("/hash")
def gerar_hash():
    return {calcular_hash_sha256(file)}


@modelos_router.get("/qtd")
def contar_elementos():
    return {"quantidade de modelos no csv": len(modelo_data)}


@modelos_router.get("/", status_code=HTTPStatus.OK)
def listar():
    if modelo_data.empty:
        return []
    return modelo_data.to_dict(orient="records")


@modelos_router.post("/", response_model=Modelo, status_code=HTTPStatus.CREATED)
def inserir(modelo: Modelo):
    global modelo_data
    if modelo.id == None:
        modelo.id = uuid.uuid4()
    elif modelo_data[modelo_data["id"] == modelo.id].empty:
        raise HTTPException(status_code=400, detail="ID já existe.")
    modelo_validado = Modelo.model_validate(modelo)
    modelo_data = append_csv(file, campos, modelo_validado.model_dump(), modelo_data)
    return modelo_validado


@modelos_router.put("/{id}", response_model=Modelo)
def atualizar(id: uuid.UUID, modelo: Modelo):
    elemento = modelo_data[modelo_data["id"] == str(id)]
    if elemento.empty:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Modelo não encontrado."
        )
    if modelo.id == None:
        modelo.id = id
    modelo_validado = Modelo.model_validate(modelo)
    modelo_data.loc[elemento.index[0]] = modelo_validado.model_dump()
    modelo_data.to_csv(file, index=False)
    return modelo_validado


@modelos_router.delete("/{id}")
def excluir(id: uuid.UUID):
    global modelo_data
    elemento = modelo_data[modelo_data["id"] == str(id)]
    if elemento.empty:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Modelo não encontrado."
        )
    modelo_data = modelo_data.drop(index=elemento.index[0])
    modelo_data.to_csv(file, index=False)
    return {"detail": "Modelo excluído com sucesso"}
