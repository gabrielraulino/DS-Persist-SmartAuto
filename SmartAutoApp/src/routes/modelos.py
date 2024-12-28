from http import HTTPStatus
from fastapi import APIRouter, HTTPException
import uuid
from utils.file_handler import read_csv, append_csv, write_csv
from models.modelo import Modelo

modelos_router = APIRouter()
campos = ["id", "nome"]
file = "src/storage/modelos.csv"
modelo_data = read_csv(file)


@modelos_router.get("/modelos/")
def listar():
    if modelo_data.empty:
        return []
    return modelo_data.to_dict(orient="records")


@modelos_router.post("/modelos/", response_model=Modelo, status_code=HTTPStatus.CREATED)
def inserir(modelo: Modelo):
    global modelo_data
    if not modelo.id:
        modelo.id = str(uuid.uuid4())
    elif (
        "id" in modelo_data.columns
        and modelo_data[modelo_data["id"] == modelo.id].empty
    ):
        raise HTTPException(status_code=400, detail="ID já existe.")
    modelo_validado = Modelo.model_validate(modelo)
    modelo_data = append_csv(file, campos, modelo_validado.model_dump(), modelo_data)
    return modelo_validado
